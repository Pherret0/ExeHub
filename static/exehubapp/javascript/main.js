<!-- Created By Travis -->
$(document).ready(function(){
    $('#dropdown').click(function (e) {
        e.preventDefault();
        document.getElementById('dropdownlinks').style.display = "block";
    });

    $(window).click(function(e){
        if(!($(e.target).is('#dropdownlinks') || $(e.target).is('img'))){
            document.getElementById('dropdownlinks').style.display ="none";
        }
    });

});