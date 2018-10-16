var items_to_borrow = {};

$(document).ready(function() {
    $("#add_button").on('click', function(){
        var item = $("#item").val();
        var quantity = $("#quantity").val();
        var ret_date = $("#ret-date").val();
        var today = new Date();
        var date_to_ret = new Date(parseDate(ret_date));
        if(today > date_to_ret){
            alert("Return date must be after today or today");
            return;
        }
        if(item && quantity && ret_date){
            var html_div = `<button ondblclick="removeItem(this)" type="button" class="btn btn-success added-item">${item} <span class="badge">${quantity} : ${ret_date}</span></button>`;
            $(".items").prepend(html_div);
            $("#item").val("");
            $("#quantity").val("1");
        }
    });

    $("#item").keyup(function(){
        equipment = $("#item").val();
        if(equipment){
            $.ajax({
                type          : 'POST',
                url           : '/search-equipment/',
                data          : {
                                    "equipment" : equipment,
                                    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                },
                success       : function(data, textStatus, jqXHR){
                    $(".search-equipment").html(data);
                    $(".search-equipment").show();
                },
                error         : function(xhr, status, error){
                    alert("Error");
                },
                dataType      : 'text'
            });
        }
        else{
            $(".search-equipment").hide();
        }

    });

    $("#submit").on('click', function(){
        extractFormFields();
    });

    $("#matricule").keypress(function(){
        $("#error").hide();
    });

    $("#tel").keypress(function(){
        $("#error").hide();
    });

    $("#ret-date").focus(function(){
        $("#error").hide();
    });
});

function removeItem(element){
    $(element).remove();
}

function extractFormFields(){
    items_to_borrow = {};
    $(".items button").each(function(){
        var each_item = $(this).html();
        // var regexp = /(\w+)\s<span(\W+)\d+<\/span>/g;
        var regexp = /(.+)\s<span\W.+">(\d+) : (.+)<\//g; //regular expression to extract the item and its quantity
        var myArray = regexp.exec(each_item);
        items_to_borrow[`${myArray[1]}`] = myArray[2] + "," + myArray[3];
    });

    var matricule = $("#matricule").val();
    var tel = $("#tel").val();
    if(!matricule || !tel || jQuery.isEmptyObject(items_to_borrow || matricule.length != 8)){
        $("#error").show();
        return;
    }

    $("#error").hide();
    $(".body-wrapper").show();
    $(".circle-animate-loading").show();
    //send the information to the server
    $.ajax({
        type          : 'POST',
        url           : '/confirm-equipment-borrow/',
        data          : {
                            'matricule'    :  matricule,
                            'tel'          :  tel,
                            'items_to_borrow': JSON.stringify(items_to_borrow),
                            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
        },
        success       : function(){
            $(".body-wrapper").hide();
            $(".circle-animate-loading").hide();
            alert("success");
            emptyFields();          //remove all writings inputted by the user
        },
        error         : function(xhr, status, error){
            $(".body-wrapper").hide();
            $(".circle-animate-loading").hide();
            alert("Message won't go");
            alert(xhr.responseText);
            alert("success");
            emptyFields();
        },
        dataType      : 'text'
    });
}

function emptyFields(){
    $("#matricule").val("");
    $("#tel").val("");
    $("#ret-date").val("");
    $("#item").val("");
    $("#quantity").val("1");
    $(".items").empty();
}

function equipmentSelected(id, equipment){
    $(".search-equipment").hide();
    $("#item").val(equipment);
}

function parseDate(s) {
    var b = s.split(/\D/);
    return new Date(b[0], --b[1], b[2]);
}