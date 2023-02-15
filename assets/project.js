$(document).ready(function(){

$.getJSON('/specializationdisplayalljson',function(data){
//    alert(JSON.stringify(data.result))
    data.result.map((item)=>{
    $('#specialization').append($('<option>').text(item.specialization).val(item.specializationid))


//        alert(item.specialization)

    })
})



})