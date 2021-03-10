<!-- Created By Kai & Jack-->
$(document).ready(function(){
    $('#register').submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'addUser/',
            data: $(this).serialize(),
            success: function(response){
                window.location.href = "/login/";
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

var high_date = '2005-01-01';
var low_date = new Date(1900, 0, 0);

// Check whether form is valid and ready to be submitted
var interval = 3000;
var timer = window.setInterval(function(){
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

