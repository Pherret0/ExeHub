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