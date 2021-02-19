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
                alert("Event successfully added!");
            }
        });
   });
});