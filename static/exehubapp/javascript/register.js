<!-- Created By Kai -->
$(document).ready(function(){
    $('#register').submit(function (e) {
        alert("Sending...")
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'addUser/',
            data: $(this).serialize(),
            success: function(response){
                alert("Registered successfully!");
                window.location.href = "/";
            }
        });
   });

    // Get the HTML elements
    var popup = document.getElementById("popup");
    var button = document.getElementById("button");
    var span = document.getElementsByClassName("close")[0];

    // When user clicks help, open the popup
    button.onclick = function() {
      popup.style.display = "block";
    }

    // When the user clicks on x, close the modal
    span.onclick = function() {
      popup.style.display = "none";
    }

    // When the user clicks anywhere outside of the popup, close it
    window.onclick = function(event) {
      if (event.target == popup) {
        popup.style.display = "none";
      }
    }
});

var interval = 400;
var timer = window.setInterval(function(){
    // your code goes here ...
    if(document.getElementById("register").checkValidity()){
        document.getElementById("submit").style.border = "2px solid green";
    }else{
        document.getElementById("submit").style.border = "2px solid red";
    }


}, interval);

function verifyUniqueEmail() {
    var email = document.getElementById("email").value;
    $.ajax({
        type: 'POST',
        url: 'verifyuniqueemail/',
        data: {email: email},
        dataType: "json",
        success: function (response) {
            if (response == 0) {
                document.getElementById("duplicate_user").style.display="none";
                document.getElementById("email").setCustomValidity("");
            } else {
                document.getElementById("duplicate_user").style.display="block";
                document.getElementById("email").setCustomValidity("Invalid field.");

            }
        }
    });
}

