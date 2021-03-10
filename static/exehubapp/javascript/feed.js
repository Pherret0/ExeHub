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
        let post_id = $(this).closest('.post').attr('id');
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'upvote/',
            context: this,
            data: {post_id: post_id},
            dataType: "json",
            success: function(response) {

                if (response['votes'] === -1) {
                    alert("something went wrong upvoting");
                }else {
                    let upvote = $(this).siblings().children('.count');
                    upvote.text(response['votes']);
                    if (response['change'] === 1) {
                        $(this).children('.upvote_img').attr('src', 'static/exehubapp/img/icons/post/upvote arrow clicked.png');
                    } else{
                        $(this).children('.upvote_img').attr('src', 'static/exehubapp/img/icons/post/upvote arrow wip 1.png');
                    }
                }
            }
        });
   });



    $('#feed').on('click', '.open', function(e){
        let id = $(this).closest('.post').attr('id');
        window.location.href = "/post/" + id;
    })
});