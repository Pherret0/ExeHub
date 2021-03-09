<!-- Created By Travis -->
$(document).ready(function(){
    $('.comments').click(function (e) {
        //window.location.replace("/events/" + $(this).attr('id'));
   });


    $('.comments').on('click', function(e){
        e.preventDefault();
        document.getElementById("pop_out_post").style.display = "block"; // shows menu
        document.getElementById("pop_out_post").innerHTML = "events/1.html"
        $('.pop_out_post').load("events/1");

        $('.content').on('click', function(e){ // when clicked out
            e.preventDefault();
            if ($(e.target).is('.content')) {
                document.getElementById("pop_out_post").style.display = "none";
            }

        });
    });

    $('#feed').on('click', '.upvote', function (e) {
        alert("Hello!")
        let post_id = $(this).closest('.post').attr('id');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'upvote/',
            context: this,
            data: {post_id: post_id},
            dataType: "json",
            success: function(response) {
                alert("Response!")
                if (response == 0) {
                    let upvote =  $(this).siblings().children('.count');
                    if (upvote.text() == 'None') {
                        upvote.nodeValue = 1;
                    } else {
                        let num = upvote.text();
                        num++;
                        upvote.text(num);
                        $(this).children('.upvote_img').attr("src", "{% static 'exehubapp/img/icons/upvote arrow clicked.png' %}");
                    }
                }else {
                alert("something went wrong upvoting");
                }
            }
        });
   });



    $('#feed').on('click', '.open', function(e){
        let id = $(this).closest('.post').attr('id');
        window.location.href = "/post/" + id;
    })
});