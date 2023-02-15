$(document).ready(function(){

    $.getJSON('/fetchallstates',function(data){
//         alert(JSON.stringify(data))
        data.result.map((item)=>{

          $('#sourcestate').append(
            $('<option>').text(item.statename).val(item.stateid)
            );
        });
        $("#sourcestate").material_select();

      });

      $('#sourcestate').change(function(){
        $('#sourcecity').empty()
        $('#sourcecity').append($('<option disable selected>').text('Choose your City'))

        $.getJSON("/fetchallcity",{stateid:$('#sourcestate').val()},function(data){

          data.result.map((item)=>{

            $('#sourcecity').append(
              $('<option>').text(item.cityname).val(item.cityid)
              );
          });
        $("#sourcecity").material_select();
        });

      });

});