var i=0
var ques=[]
var subques=[]
var result=[]

// Sub-Questions
function subquestion()
{
  var qnum=1

  subques=ques[i].subquestions.split('#')
  var shtm=""
  var blockname=['Normal','Mild','Modrate','Severe','Extreme']
  for(j=0;j<subques.length;j++){
    shtm+=`<div class='col s12' style="margin-top: 10px;margin-bottom:5px;font-size:12px;font-weight:600">Q${(j+1)}: ${subques[j]}</div>`
    for(block=0;block<5;block++){
    shtm+=`<div value='${block+1}' class="rate${i}${j}${block} col blocks block-color"  style="margin-left:8px;width:65px;height:58px;font-weight: 500;" id="rate${qnum}${block}">${blockname[block]}<br>${block+1}</div>`
    }
    qnum+=1
  }
  $('#subquestiondiv').html(shtm)

  $('#heading').html($('#splname').val()+' '+'index'+' '+(i+1)+'/'+ques.length)

}

$(document).ready(function(){

$.getJSON('/userquestion',{splid:$('#spl').val()},function(data){
//alert(JSON.stringify(data))
// Questions
  ques=data.result

  htm="Q"+ques[i].questionnumber+": "+ques[i].question
  $('#questiondiv').html(htm)

  // Create Key and Value in the list For Score
  for(j=0;j<ques.length;j++){
    subques=ques[j].subquestions.split('#')
    temp2={}
    for(k=0;k<subques.length;k++){
        temp="rate"+String(k)
        temp2[temp]=0

    }
    result.push(temp2)
  }

  // Score
  totalsum=0
  outof=0
  $.each(result[i], function(key, value) {
  totalsum+=parseInt(value)
  outof+=5
  })
  $('#currentscore').html("Score "+String(totalsum)+"/"+String(outof))


  subquestion()
})

// Next Button Manupilation
$('#btnnext').click(function(){
  i++
  if(i<ques.length){
  htm="Q"+ques[i].questionnumber+":"+ques[i].question
  $('#questiondiv').html(htm)
  subquestion()
   }

//submitscore
//alert(ques.length+","+(i+1))
  if(i+1>ques.length)
  {
$.getJSON('/submitscore',{'score':JSON.stringify(result)},function(data){
         alert(data.result)
         payment(data.username,data.mobileno,data.email)

      })
  }


// previous button div color
$.each(result[i],function(key,value)
         {
            // console.log(value,key)
            if(value!=0){
            $('.rate'+String(i)+key[key.length-1]+String(value-1)).removeClass('block-color').addClass('block-onclick-color')
            //  alert('.rate'+String(i)+key[key.length-1]+String(value-1))
            }
         })


// Previous Button Manupilation
  if(ques.length>=1){

          $('#btnnext1').removeClass('col s12').addClass('col s6')
           $('#btnprev').addClass('col s6')
           temp1=`<button id="btnprev1" style="width:100%;border-radius:20px;background:rgb(17, 194, 214);" class=" waves-effect wave-light btn" type="button" name="action">Preivous</button>`
           $('#btnprev').html(temp1)
        }

  $('#btnprev1').click(function(){
  i--
  if(i<ques.length){
  htm="Q"+ques[i].questionnumber+":"+ques[i].question
  $('#questiondiv').html(htm)

  subquestion()
}

// previous button div color
$.each(result[i],function(key,value)
         {
            // console.log(value,key)
            if(value!=0){
            $('.rate'+String(i)+key[key.length-1]+String(value-1)).removeClass('block-color').addClass('block-onclick-color')
            //  alert('.rate'+String(i)+key[key.length-1]+String(value-1))
            }
         })

 if(i==0){
    $('#btnprev').html('')
    $('#btnprev').removeClass('col s6')
    $('#btnnext1').removeClass('col s6').addClass('col s12')
  }
  })

})




// div color change
function onclicks(blockid){

    temp=blockid.slice(0,blockid.length-1)
//    alert(temp)
    for(k=0;k<5;k++){
        $("#"+temp+String(k)).removeClass('block-onclick-color').addClass('block-color')
    }
    $("#"+blockid).removeClass('block-color').addClass('block-onclick-color')



}


$(document).click(function(event){

        //change div color
        blockid=event.target.id
        // alert(blockid)

        //onclick div color change
        len=blockid.length
        if("rate"===blockid.slice(0,len-2)){
            onclicks(blockid)
            temp3="rate"+String(parseInt(blockid[len-2])-1)
            result[i][temp3]= parseInt(blockid[len-1])+1
        }
        console.log(result)

        // Score
        totalsum=0
            outof=0
            $.each(result[i],function(key, value){
              totalsum+=parseInt(value)
              outof+=5
            })
            $('#currentscore').html("Score "+String(totalsum)+"/"+String(outof))

    })


/**********Payments******************/

 function payment(username,mobileno,email){
    var options = {
	"key": "rzp_test_GQ6XaPC6gMPNwH",
	"amount": 100*100, // Example: 2000 paise = INR 20
	"name": "MedAsist",
	"description": "Payment for Subscription",
	"image": "/static/logo1.png",// COMPANY LOGO

	"handler": function (response) {
		console.log(response);

        // AFTER TRANSACTION IS COMPLETE YOU WILL GET THE RESPONSE HERE.
	},
	"prefill": {
		"name": username, // pass customer name
        "email": email,
		"contact": mobileno,//customer phone no.
	},
	"notes": {
		"address": "address" //customer address
	},
	"theme": {
		"color": "rgb(17, 194, 214)" // screen color
	}
};
console.log(options);
var propay = new Razorpay(options);
propay.open();



}

   /**************************/

})




