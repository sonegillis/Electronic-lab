$(document).ready(function() {

    //search each key pressed to the backend system
    $("#search_bar").keyup(function(){
        var searching_by = $("#searching_by").val();
        var value = $("#search_bar").val();
        if(value==""){
            $(".searchtransaction_result").hide();
            return;
        }
        $.ajax({
            type          : 'POST',
            url           : '/search-borrow-transaction/',
            data          : {
                                'searching_by' :  searching_by,
                                'value'     :  value,
                                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success       : function(data, textStatus, jqXHR){
                $(".searchtransaction_result").show();
                $(".searchtransaction_result").html(data);
            },
            error         : function(xhr, status, error){
                alert("Error");
            },
            dataType      : 'HTML'
        });
    });

});    

function returnEquipment(id, equipment, quantity){
    var confirm_return = confirm(`Are you sure want to return ${quantity} ${equipment}`);
    if(confirm_return){
        $.ajax({
            type          : 'POST',
            url           : '/return-equipment/',
            data          : {
                                'id'        : id,
                                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success       : function(data, textStatus, jqXHR){
                $("#"+id).remove();
                if($("#match_table").html().indexOf("</tr>")==-1){
                    $(".searchtransaction_result").hide();
                }
                alert(`${quantity} ${equipment} have been returned`);
            },
            error         : function(xhr, status, error){
                alert("Equipment Cannot be returned");
            },
            dataType      : 'text'
        });
    }
    return;
}