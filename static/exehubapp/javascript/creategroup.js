<!-- Created By Travis -->
$(document).ready(function(){
    $('#uni_groups').submit(function (e) {
        alert("Sending...")
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'create/',
            data: $(this).serialize(),
            success: function(response){
                alert("Group successfully created!");
            }
        });
   });
});
