$(document).ready(function() { 
    $(".json").prop('disabled', true);
    $('input[type="radio"]').click(function() { 
        var inputValue = $(this).attr("value");
        if (inputValue == "text") {
          $(".json").prop('disabled', true);
          $(".text").prop('disabled', false);
          console.log("help");

        }
        else if (inputValue == "json") {
          $(".text").prop('disabled', true);
          $(".json").prop('disabled', false);
        }
    }); 
}); 

function callApi() {
  var serializedData;
  var formData;
  event.preventDefault();
  var format = $('input[type="radio"]:checked').attr("value");
  if (format == "text") {
    formData = $("#textform").serialize();
    $("#textform:input").each(function(){
      serializedData = serializedData + $(this).val();
     });
  }

  else if (format == "json") {
    formData = $("#jsonform").serialize();
    $("#jsonform:input").each(function(){
      serializedData = serializedData + $(this).val();
     });
  }

  console.log(formData);
  console.log(JSON.stringify(formData));
  console.log("http://127.0.0.1:8000/clients/api/search/"+formData)

  let request = new XMLHttpRequest();
  
  request.open("GET", "http://127.0.0.1:8000/clients/api/search/?title=lord");
  request.setRequestHeader('Authorization', 'Token b9d0859ce2420ed4c69878b47abebcbd056e627e');
  request.send();
  request.onload = () => {
    console.log(request);
    if (request.status == 200) {
      console.log(JSON.parse(request.response));
    } else {
      console.log(`error ${request.status} ${request.statusText}`)
    }
  }
}

