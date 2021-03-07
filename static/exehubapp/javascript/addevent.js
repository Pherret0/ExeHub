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
                if (response == 0){
                    alert("Event created successfully");
                } else{
                    alert("Error creating event");
                }
            }
        });
   });

    var interval = 400;
    var timer = window.setInterval(function() {

        if (document.getElementById("eventForm").checkValidity()) {
            document.getElementById("submit").style.border = "2px solid green";
        } else {
            document.getElementById("submit").style.border = "2px solid red";
        }

        var min_attendees = document.getElementById("attendees_min").value;
        var max_attendees = document.getElementById("attendees_max").value;

        if (min_attendees > max_attendees){
            document.getElementById("attendees_min").setCustomValidity("Invalid field.");
            document.getElementById("attendees_max").setCustomValidity("Invalid field.");
        }else{
            document.getElementById("attendees_min").setCustomValidity("");
            document.getElementById("attendees_max").setCustomValidity("");
        }

        var  start = document.getElementById("start").value;
        var end = document.getElementById("end").value;

        if (start > end){
            document.getElementById("start").setCustomValidity("Invalid field.");
            document.getElementById("end").setCustomValidity("Invalid field.");
        }else{
            document.getElementById("start").setCustomValidity("");
            document.getElementById("end").setCustomValidity("");
        }
    }, interval);

    //Set default time of start and end input fields to current time
    //and current time + 1 hour.
    var now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('start').value = now.toISOString().slice(0,16);
    now.setHours(now.getHours()+1);
    document.getElementById('end').value = now.toISOString().slice(0,16);
});

//Functions for displaying the relevant form based.
function showTextForm() {
    document.getElementById("start_section").style.display = "none";
    document.getElementById("start").required = false;
    document.getElementById("end_section").style.display = "none";
    document.getElementById("end").required = false;
    document.getElementById("location_section").style.display = "none";
    document.getElementById("location").required = false;
    document.getElementById("attendees_min_section").style.display = "none";
    document.getElementById("attendees_max_section").style.display = "none";
    document.getElementById("image_section").style.display = "none";
    document.getElementById("image").required = false;
    document.getElementById("type").value = "text";

    document.getElementById("event_button").style.backgroundColor = "transparent";
    document.getElementById("text_button").style.backgroundColor = "rgba(108, 163, 247, 1)";
    document.getElementById("text_button").style.color = "white";
    document.getElementById("event_button").style.color = "black";
    document.getElementById("image_button").style.color = "black";
    document.getElementById("image_button").style.backgroundColor = "transparent";
}

function showEventForm() {
    document.getElementById("start_section").style.display = "block";
    document.getElementById("start").required = true;
    document.getElementById("end_section").style.display = "block";
    document.getElementById("end").required = true;
    document.getElementById("location_section").style.display = "block";
    document.getElementById("location").required = true;
    document.getElementById("attendees_min_section").style.display = "block";
    document.getElementById("attendees_max_section").style.display = "block";
    document.getElementById("image_section").style.display = "block";
    document.getElementById("image").required = false;
    document.getElementById("type").value = "event";

    document.getElementById("event_button").style.backgroundColor = "rgba(108, 163, 247, 1)";
    document.getElementById("text_button").style.color = "black";
    document.getElementById("event_button").style.color = "white";
    document.getElementById("image_button").style.color = "black";
    document.getElementById("text_button").style.backgroundColor = "transparent";
    document.getElementById("image_button").style.backgroundColor = "transparent";
}

function showImageForm() {
    document.getElementById("start_section").style.display = "none";
    document.getElementById("start").required = false;
    document.getElementById("end_section").style.display = "none";
    document.getElementById("end").required = false;
    document.getElementById("location_section").style.display = "none";
    document.getElementById("location").required = false;
    document.getElementById("attendees_min_section").style.display = "none";
    document.getElementById("attendees_max_section").style.display = "none";
    document.getElementById("image_section").style.display = "block";
    document.getElementById("image").required = true;
    document.getElementById("type").value = "image";

    document.getElementById("event_button").style.backgroundColor = "transparent";
    document.getElementById("text_button").style.backgroundColor = "transparent";
    document.getElementById("text_button").style.color = "black";
    document.getElementById("event_button").style.color = "black";
    document.getElementById("image_button").style.color = "white";
    document.getElementById("image_button").style.backgroundColor = "rgba(108, 163, 247, 1)";
}





