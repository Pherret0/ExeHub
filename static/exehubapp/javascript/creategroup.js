<!-- Created By Travis -->
$(document).ready(function()
{
    $('#uni_groups').submit(function(e)
    {
        alert("Creating Group...")
        e.preventDefault();
        $.ajax(
        {
            type: 'POST',
            url: 'create/',
            data: $(this).serialize(),
            success: function(response){
                if (response == "0"){
                    alert("Group created successfully");
                } else{
                    alert("Duplicate group");
                }
            }
        });
    });
});
