from django.shortcuts import render
from .forms import LoginForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import EquipmentBorrowTransactions, ModemState, ModemImeiNumber, Equipment
from django.db.models import Q
from django.contrib.auth import(
    authenticate,
    login,
    logout
)
from .pysms import Modem
import json
import socket
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


orange_smsc = "+23769900002"
mtn_smsc = "+237670000002"
msg_list = []

# login page view
def loginView(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # authenticate user
        user = authenticate(username=username, password=password)

        # no authentication is none
        if user is not None:
            template_name = "homepage.html"
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            template_name = "login.html"
            form = LoginForm()
            context = {
                "form"  :   form,
                "error" :   "Username or password incorrect"
            }
            return render(request, template_name, context)

    if request.method == "GET":
        # take user to home page if already authenticated
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        form = LoginForm()
        context = {
            "form"  :  form
        }
        template_name = "login.html"
        return render(request, template_name, context)

# logout view
def logoutView(request):
    if request.user.is_authenticated():
        request.session.flush()
        logout(request)
        print("User is authenticated")
        return HttpResponseRedirect(reverse('login'))
    
    else:
        return HttpResponseRedirect(reverse('login'))

# home page view
@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def homeView(request):
    print(request.user.is_authenticated())
    template_name = "homepage.html"
    return render(request, template_name)

@login_required(login_url='/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def borrowEquipmentView(request):
    template_name = "borrowequipment.html"
    return render(request, template_name)


# method that recieves the request for equipment borrowing

def processBorrowTransaction(request):
    global msg_list
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 10000))
    user = request.user                     # get which user is try to perform this transaction
    donors_name = user.first_name + " " + user.last_name   # full name of person that gave out equipment

    tel = request.POST["tel"]
    number_type = numberTypePredict(tel)
    print(number_type)
    
    if number_type == None:
        return HttpResponse("Number must be a 9 digit MTN or Orange number and must begin with 6", status=404)

    matricule = request.POST["matricule"]
    items_to_borrow_json = request.POST["items_to_borrow"]
    items_to_borrow_dict = json.loads(items_to_borrow_json)       # convert json object to python dictionary for extraction of keys and values

    formatted_items_for_msg = ""

    for item in items_to_borrow_dict.keys():
        # save transaction into database
        value = items_to_borrow_dict[item].split(",")       # this has the quantity and date seperated by a comma
        formatted_items_for_msg = formatted_items_for_msg + item + ":" + value[0] + "(" + value[1] + ")\n"
        EquipmentBorrowTransactions(
            matricule = matricule,
            tel = tel,
            ret_date = value[1],
            item = item,
            quantity = value[0],
            given_by = user
        ).save()


    """
        Example of message to send is 
        *****************************
        FE14A125 you have borrowed the following from the lab
        Multimeter:1(2018-11-03)
        PIC16F877A":4(2018-11-03)
        from Mr./Dr. Tsafack Pierre.
        Thanks!!!
    """

    message = matricule + " you have borrowed the following from the lab "
    message = message + formatted_items_for_msg + " from Mr./Dr. " + donors_name
    message = message + "\nThanks!!!"

    data = {
            "message" : message,
            "phoneNumber": tel,
    }

    s.sendall(json.dumps(data).encode("utf-8"))
    sleep(1)
    s.close() 

    return HttpResponse("")

def searchBorrowTransaction(request):
    value = request.POST["value"]
    searching_by = request.POST["searching_by"]     # this can be by equipment, phone number or matricule
    template_name = "searchtransactionresult.html"

    print("*******")
    print(value)

    if searching_by == "matricule":
        #query table based on matricule and if it has not been refunded
        qs = EquipmentBorrowTransactions.objects.filter(Q(matricule__istartswith=value) & Q(returned=False))
        
    if searching_by == "tel":
        #query table based on tel and if it has not been refunded
        qs = EquipmentBorrowTransactions.objects.filter(Q(tel__istartswith=value) & Q(returned=False))
        
    if searching_by == "equipment":
        #query table based on equipment and if it has not been refunded
        qs = EquipmentBorrowTransactions.objects.filter(Q(item__istartswith=value) & Q(returned=False))
    
    print(qs.count())

    return render(request, template_name, {"qs": qs})

def returnEquipment(request):
    user = request.user
    transaction_id = request.POST["id"]
    qs = EquipmentBorrowTransactions.objects.filter(id=transaction_id).update(returned=True, returned_to=user)
    return HttpResponse("")

def searchEquipment(request):
    template_name = "searchequipment.html"
    equipment = request.POST["equipment"]

    query = Equipment.objects.filter(component__istartswith=equipment)

    return render(request, template_name, {"qs" : query})

# this method will determine if the phone number is an 
# for example either MTN or ORANGE
# It'll return 0 for MTN, 1 for ORANGE
# It can be modified when another network is needed
def numberTypePredict(tel):
    # will use these codes to differentiate between MTN numbers and 
    # ORANGE numbers so as the send the sms with the right modem
    orange_prefix_codes = [69,656,655,657]
    mtn_prefix_codes = [67,650,651,652,653,654]

    if int(tel[0:2]) in mtn_prefix_codes or int(tel[0:3]) in mtn_prefix_codes:
        return 0

    if int(tel[0:2]) in orange_prefix_codes or int(tel[0:3]) in orange_prefix_codes:
        return 1
    
    else:
        return None
    
# this method will determine if the message is longer than 150 characters
# the function will split the message ensuring that longer messages can
# be sent in a more organised format
# it can be better by using multipart SMS which is beyond the scope of 
# this function 

def formatSMS(msg, start_count):
    global msg_list         # making it global since it has to be eddited in function
    if len(msg) <= start_count: 
        msg_list.append(msg.strip("\n").strip(" ")) # append the message like that if it less than 140 chars
        return           
    if msg[start_count] != " " or msg[start_count] != "\n":  # testing if we are on a newline or a space
        for i in range(start_count+1, len(msg)):    # keep looping until you find a newline or a space char
            if msg[i] == " " or msg[i] == "\n":  
                msg_list.append(msg[0: i].strip("\n").strip(" "))
                return formatSMS(msg[i+1:], 140)
            else:
                pass
    else:
        return formatSMS(msg[start_count+1:], 140)  # if we fell on a space of newline we can continue recursively


def testView(request):
    template_name = "weatherlogin.html"
    return render(request, template_name)
