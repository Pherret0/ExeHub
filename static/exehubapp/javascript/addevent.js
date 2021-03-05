<!-- Created By Travis -->
$(document).ready(function(){
    $('#eventForm').submit(function (e) {
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
