<!-- Created By Travis -->
$(document).ready(function()
{
    $('#uni_groups').submit(function(e) {
        e.preventDefault();
        $.ajax(
        {
            type: 'POST',
            url: 'create/',
            data: $(this).serialize(),
            success: function(response){
                if (response == 0){
                    alert("Group created successfully");
                } else{
                    alert("Duplicate group");
                }
            }
        });
    });
});

function verifyUniqueGroup() {
    var groupName = document.getElementById("group_name").value;
    $.ajax({
        type: 'POST',
        url: 'verifyunique/',
        data: {groupName: groupName},
        dataType: "json",
        success: function (response) {
            if (response == 0) {
                document.getElementById("duplicate_group").style.display="none";
                document.getElementById("group_name").setCustomValidity("");
            } else {
                document.getElementById("duplicate_group").style.display="block";
                document.getElementById("group_name").setCustomValidity("Invalid field.");
            }
        }
    });
}

var interval = 400;
var timer = window.setInterval(function(){
    if(document.getElementById("uni_groups").checkValidity()){
        document.getElementById("submit").style.border = "2px solid green";
    }else{
        document.getElementById("submit").style.border = "2px solid red";
    }
}, interval);
