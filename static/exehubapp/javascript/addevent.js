<!-- Created By Travis -->
$(document).ready(function(){
    $('#events').submit(function (e) {
        alert("Sending...")
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'create/',
            data: $(this).serialize(),
            success: function(response){
                if (response == "0"){
                    alert("Event created successfully");
                } else{
                    alert("Something went wrong");
                }
            }
        });
   });
});
