<!-- Created By Jack -->
$(document).ready(function()
{
    $('#update_email').submit(function(e) {

        e.preventDefault();
        $.ajax(
        {
            type: 'POST',
            url: 'updateemail/',
            data: $(this).serialize(),
            success: function(response){
                if (response == 0){
                    alert("Email Updated");
                } else if (response == 2) {
                    alert("Incorrect Password, Please Try Again");
                }else{
                    alert("An error occurred updating email");
                }
            }
        });
    });

    $('#update_password').submit(function(e) {

        e.preventDefault();
        $.ajax(
        {
            type: 'POST',
            url: 'updatepassword/',
            data: $(this).serialize(),
            success: function(response){
                if (response == 0){
                    alert("Password Updated");
                } else if (response == 2) {
                    alert("Incorrect Current Password, Please Try Again");
                } else
                {
                    alert("An error occurred updating password");
                }
            }
        });
    });

    $('#delete_account').submit(function(e) {

        e.preventDefault();
        $.ajax(
        {
            type: 'POST',
            url: 'deleteaccount/',
            data: $(this).serialize(),
            success: function(response){
                if (response == 0){
                    alert("Account Deleted");
                } else if (response == 2) {
                    alert("Incorrect Password, Please Try Again");
                }else{
                    alert("An error occurred deleting account");
                }
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

var interval = 400;
var timer = window.setInterval(function() {
    if (document.getElementById("update_email").checkValidity()) {
        document.getElementById("submit").style.border = "2px solid green";
    } else {
        document.getElementById("submit").style.border = "2px solid red";
    }

    if (document.getElementById("update_password").checkValidity()) {
        document.getElementById("submit_pass").style.border = "2px solid green";
    } else {
        document.getElementById("submit_pass").style.border = "2px solid red";
    }
}, interval);







