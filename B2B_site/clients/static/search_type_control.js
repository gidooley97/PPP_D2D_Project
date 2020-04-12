$(document).ready(function() { 
    $(".json").prop('disabled', true);
    $('input[type="radio"]').click(function() { 
        var inputValue = $(this).attr("value");
        if (inputValue == "text") {
          $(".json").prop('disabled', true);
          $(".text").prop('disabled', false);

        }
        else if (inputValue == "json") {
          $(".text").prop('disabled', true);
          $(".json").prop('disabled', false);
        }
    }); 
}); 

var coll = document.getElementsByClassName("container");
var i;

