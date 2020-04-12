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

$("#textform").submit(function(e) {
  e.preventDefault();
});

$("#jsonform").submit(function(e) {
  e.preventDefault();
});

function callApi() {
  var format = $('input[type="radio"]:checked').attr("value");
  console.log("help")
  if (format == "text") {
    $("#textform:input").each(function(){
      console.log(JSON.stringify($(this))); // This is the jquery object of the input, do what you will
     });
  }

  else if (format == "json") {
    //
  }
}

