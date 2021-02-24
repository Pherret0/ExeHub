<!-- Created By Kai -->
$(document).ready(function(){
    $('#register').submit(function (e) {
        var password = document.forms["register"]["password"].value;
        alert(password);
        if (password == "") {
            alert("Password must be filled out");
            return false;
        }
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