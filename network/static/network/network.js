document.addEventListener('DOMContentLoaded', function(){

    $(document).ready(function(){

        $(".profile").on("click", ".follow", function( event ) {
            event.preventDefault();
            const element = event.target;
            followOrNot = element.dataset.follow
            const parent = element.parentElement;         
            const profile_id = parent.dataset.profile_id;   
            follow(profile_id, followOrNot);            
        });

    }); 

    $(document).ready(function(){

        $(".post").on("click", ".like, .unlike", function( event ) {
            event.preventDefault();
            const element = event.target;
            like = element.className;
            const parent = element.parentElement.parentElement;         
            const post_id = parent.dataset.post_id;   
            update_likes(post_id, like);            
        });

    }); 


    document.querySelectorAll('.edit').forEach(edit_button =>{     
        edit_button.addEventListener('click', event => {

            const element = event.target;
            const parent = element.parentElement;
            parent.querySelector('.post_text').style.display = 'none';
            parent.querySelector('.edit_post').style.display = 'block';

            const post_id = parent.dataset.post_id;

            parent.querySelector('.save').addEventListener('click', () => {
                edit_post(post_id);
                event.preventDefault();
            });
        })
    })
});



function edit_post(post_id){
    
    parent = document.querySelector(`[data-post_id = "${post_id}"]`)
    
    const edit_post_text= parent.querySelector('.edit_post_text').value;

    call='/edit_post/'+post_id;

    fetch(call, {
        method: 'PUT',
        body: JSON.stringify({
            text: edit_post_text
        })
    })
    
    .then(response =>{
        console.log(`PUT request status: ${response.status}`);

        if (response.status == '204'){
            fetch(call)
            .then(response => response.json())
            .then(post =>{
                parent.querySelector('.post_text').innerHTML= `<p style="padding-left:5px;">${post.text}</p>`;
            })
        }
    })
    parent.querySelector('.post_text').style.display = 'block';
    parent.querySelector('.edit_post').style.display = 'none';
}


function update_likes(post_id, like){

    parent = document.querySelector(`[data-post_id = "${post_id}"]`)
    call='/edit_post/'+post_id;

    if (like.includes('like')){

        if(like.includes('unlike')){

            fetch(call, {
                method: 'PUT',
                body: JSON.stringify({
                    unlike: true
                })
            })
    
            .then(response =>{
                console.log(`PUT request status: ${response.status}`);
    
                if (response.status == '204'){
                    fetch(call)
                    .then(response => response.json())
                    .then(post =>{
                        parent.querySelector('.likes_count').innerHTML = `${post.likes} Likes`;
                        parent.querySelector('.liked').innerHTML = `<i style="color: #007bff; font-size:large ;" class="material-icons like">thumb_up</i><p class="like" style="display: inline; font-size: small; vertical-align:text-top"> Like</p>`;
                    });
                };
            });
        } else{

            fetch(call, {
                method: 'PUT',
                body: JSON.stringify({
                    like: true
                })
            })
            .then(response =>{
                console.log(`PUT request status: ${response.status}`);
    
                if (response.status == '204'){
                    fetch(call)
                    .then(response => response.json())
                    .then(post =>{
                        parent.querySelector('.likes_count').innerHTML = `${post.likes} Likes`;
                        parent.querySelector('.liked').innerHTML =`<p class="unlike" style="display: inline; font-size: small; vertical-align:text-top"> Unlike</p>`;
                    })
                }
            })
                    
        }     
    }     
}

function follow (profile_id, followOrNot){

    call='/follow/'+profile_id



    if (followOrNot=='true'){

        fetch(call, {
            method: 'PUT',
            body: JSON.stringify({
                follow: true
            })
        })
        .then(response =>{
            console.log(`PUT request status: ${response.status}`);
            if (response.status == '204'){
                document.querySelector('.follow').dataset.follow = false;
                document.querySelector('.follow').innerHTML="Unfollow"
                fetch(call)
                    .then(response => response.json())
                    .then(profile =>{
                        document.querySelector('#followers_count').innerHTML=`Followers ${profile.followers_count} Following ${profile.following_count}`;
                    });
            }
        })

    }else{
        fetch(call, {
            method: 'PUT',
            body: JSON.stringify({
                follow: false
            })
        })
        .then(response =>{
            console.log(`PUT request status: ${response.status}`);
            if (response.status == '204'){
                document.querySelector('.follow').dataset.follow = true;
                document.querySelector('.follow').innerHTML="Follow";
                fetch(call)
                    .then(response => response.json())
                    .then(profile =>{
                        document.querySelector('#followers_count').innerHTML=`Followers ${profile.followers_count} Following ${profile.following_count}`;
                    });
            }
        })
        
    }


}