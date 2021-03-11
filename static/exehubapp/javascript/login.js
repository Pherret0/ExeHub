<!-- Created By Georgia-->
$(document).ready(function(){
    $('#login').submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/login/validateLogin/',
            data: $(this).serialize(),
            success: function(response){
                if (response == 0){
                    window.location.href = "/";
                } else{
                    alert("Login unsuccessful");
                }
            }
        });
   });
});

// Check whether form is valid and ready to be submitted
var interval = 400;
var timer = window.setInterval(function(){
    if(document.getElementById("login").checkValidity()){
        document.getElementById("submit").style.border = "2px solid green";
    }else{
        document.getElementById("submit").style.border = "2px solid red";
    }
}, interval);


