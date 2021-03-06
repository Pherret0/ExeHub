<!-- Created By Travis -->
$(document).ready(function(){
    $('.comments').on('click', function(e){
        /*
            Relocated user to specific comment page for more details inc. comments
         */
        e.preventDefault();
         let id = $(this).closest('.post').attr('id');
        window.location.href = "/post/" + id;
    });

    $('#feed').on('click', '.upvote', function (e) {
        /*
            Listens for an upvote arrow to be clicked and increases/decreases upvote (if already upvoted)
            Arrow changes colour if upvote has been registered.
         */
        let post_id = $(this).closest('.post').attr('id');
        e.preventDefault();
        $.ajax({ // sending ajav request
            type: 'POST',
            url: 'upvote/',
            context: this,
            data: {post_id: post_id},
            dataType: "json",
            success: function(response) {

                if (response['votes'] === -1) { // an error, -1 is returned only when an exception occurs
                    alert("something went wrong upvoting");
                }else {
                    let upvote = $(this).siblings().children('.count'); // finding the upvote int field
                    upvote.text(response['votes']); // setting vote count to database count
                    if (response['change'] === 1) {
                        $(this).children('.upvote_img').attr('src', 'static/exehubapp/img/icons/post/upvote arrow clicked.png');
                    } else{
                        $(this).children('.upvote_img').attr('src', 'static/exehubapp/img/icons/post/upvote arrow wip 1.png');
                    }
                }
            }
        });
   });
});