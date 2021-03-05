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
            }
        });
   });
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
