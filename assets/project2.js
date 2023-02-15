$(document).ready(function(){

$.getJSON('/specializationdisplayalljson',function(data){
//    alert(JSON.stringify(data.result))
    data.result.map((item)=>{
    $('#specialization').append($('<option>').text(item.specialization).val(item.specializationid))

    })
})


$('#specialization').change(function(){
$('#question').empty()
$('#question').append($('<option disable selected>').text('-Questions-'))

$.getJSON('/questionjson',{'specializationid':$('#specialization').val()},function(data){
// alert(JSON.stringify(data))
    data.result.map((item)=>{
    $('#question').append($('<option>').text(item.question).val(item.questionid))

    })
})
})


})
