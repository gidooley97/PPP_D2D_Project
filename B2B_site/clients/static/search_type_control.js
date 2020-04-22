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

$(document).ready(function() { 
  $("button[name='drop']").click(function() {
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
});

function validateForm() {
  var w = document.forms["text"]["authors"].value
  var x = document.forms["text"]["title"].value;
  var y = document.forms["text"]["authors"].value;
  var z = document.querySelector("#myTextArea").value;
  if ((w == "" ) && (x == "" ) && (y == "") &&
  (z == "" )) {
    alert("Cannot submit blank request");
    return false;
  }
}