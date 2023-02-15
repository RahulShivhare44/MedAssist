var i=0
list=[]
$(document).ready(function()
{

// Fixing User Details as well as Doctor Details and Ques or S-Ques

$.getJSON('/patientdetails',{'userdoctorid':$('#userdoctorid').val()},function(data){

    htm=""

    htm+="<div class='row' style='margin-top:35px;display:flex;'>"
    htm+="<div class='col s6' style='width: 37%;color:black;border-radius:5px;font-weight: 400;padding: 4px;padding-left: 21px;letter-spacing:1px'>"
    htm+="Patient ID&nbsp;-&nbsp;"+data.user.userid+"<br>"
    htm+="Patient Name&nbsp;-&nbsp;"+data.user.username+"<br>"
    htm+="Patient Email&nbsp;-&nbsp;"+data.user.useremail+"<br>"
    htm+="Mobile Number&nbsp;-&nbsp;"+data.result[0].usermobile+"<br>"
    htm+="Registration Date&nbsp;-&nbsp;"+data.result[0].userdate+"<br>"
    htm+="Registration Time&nbsp;-&nbsp;"+data.result[0].usertime+"</div>"
    htm+="<div class='col s6' id='div2' style='width: 37%;color:black;font-size: 16px;font-weight: 400;padding: 4px;padding-left: 31px;margin-right: 78px;padding-top: 33px;letter-spacing: 1px;'>"
    htm+="Doctor ID&nbsp;:-&nbsp;"+data.result[0].userdoctorid+"<br>"
    htm+="Doctor Name&nbsp;:-&nbsp;"+data.doctorname+"<br>"
    htm+="Specialization&nbsp;:-&nbsp;"+data.specialization+"<br>"
    htm+="</div></div>"


    $('#details').html(htm)

    ques=""
    var totalscore=0
    for(k=0;k<data.result.length;k++){
    totalscore+=data.result[k].totalscore
        ques+="<div class='col s8'>Q"+(k+1)+"&nbsp;"+data.result[k].question+"</div><div class='col s4'>Score:&nbsp;"+data.result[k].totalscore+"/25</div>"
    }
    ques+="<div class='col s12' style='margin-top: 20px;margin-left: 270px;font-weight: 500;'>TotalScore:&nbsp;"+totalscore+"</div>"
    $('#questions').html(ques)


})

// Add Modal Content

var temp=""

$('#add').click(function(){
    i+=1
    temp=` <div class='row'>
                <div class='input-field col s4'>
                    <textarea id="instructions${i}" name='instructions${i}' class='materialize-textarea'></textarea>
                    <label for='instructions${i}'>Instructions</label>
                </div>
                <div class="input-field col s4">
                    <textarea id="medicine${i}" name="medicine${i}" class="materialize-textarea"></textarea>
                    <label for="medicine${i}">Medicines</label>
                </div>
                <div class="input-field col s4">
                    <div style="margin-top: -25px;">
                        <h6 style="font-weight: 600;">Frequency</h6>
                    </div>
                    <p>
                        <label>
                            <input value="Morning" name="frequency${i}" id="fm${i}" type="radio"  class="with-gap" />
                            <span>Morning</span>
                        </label>
                         <label>
                            <input value="AfterNoon" name="frequency${i}" id="fa${i}" type="radio" class="with-gap"/>
                            <span>After Noon</span>
                        </label>
                    </p>
                    <p>
                        <label>
                            <input value="Evening" class="with-gap" name="frequency${i}" id="fe${i}" type="radio"/>
                            <span>Evening</span>
                        </label>
                        <label>
                            <input value="Night" name="frequency${i}" type="radio" id="fn${i}" class="with-gap" />
                            <span>Night</span>
                        </label>
                    </p>
                </div>
            </div>`
            $('#table').append(temp)

})


// Submit Record
$('#submit').click(function(){

var frequency=""
for(j=0;j<=i;j++){
temp2={}
temp2['medicine']=$('#medicine'+String(j)).val()
temp2['instructions']=$('#instructions'+String(j)).val()


if($('#fm'+String(j)).is(":checked")){
    frequency="Morning"
}
else if($('#fa'+String(j)).is(":checked")){
    frequency="After Noon"
}
else if($('#fe'+String(j)).is(":checked")){
    frequency="Evening"
}
else if($('#frequency'+String(j)).is(":checked")){
    frequency="Night"
}
temp2['frequency']=frequency
list.push(temp2)

}
console.log(list)

$.getJSON('/prescriptionsubmit',{'data':JSON.stringify(list)},function(data){

  alert(JSON.stringify(data.result))
})

})





})












