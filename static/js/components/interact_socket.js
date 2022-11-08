const PostLikeCount = document.querySelectorAll('.post_like_count');
const PostCmtCount = document.querySelectorAll('.post_cmt_count');

const LikeCount = document.querySelectorAll('.like_count');
const ButtonLike = document.querySelectorAll('.button_like');

const ThisUser = document.querySelector('.navbar');

const InputCmtForm = document.querySelectorAll('.input_cmt_form');
const SubmitCmtForm = document.querySelectorAll('.submit_cmt_form');
const CmtCard = document.querySelectorAll('.comment_card .cmt');
const CmtCount = document.querySelectorAll('.post_cmt_count');
const RemoveCmt = document.querySelectorAll('.remove_cmt_post');
const CmtItem = document.querySelectorAll('.cmt_item');


// =============================like============================
function LikeCountFunct() {
    LikeCount.forEach(item => {
        PostLikeCount.forEach(count => {
            if (item.id == count.id) {
                if (parseInt(count.innerHTML) == 0) {
                    item.style.display = "none";
                }
                else{
                    item.style.display = "block";
                }
            }
        })
    })
}
LikeCountFunct();


// ==========send like===========
ButtonLike.forEach(button => {
    switch (button.classList.contains("like")) {
        case true:
            var value_like=true;
            button.addEventListener('click', () => {
                if (value_like) {
                    button.classList.remove("like");
                    button.classList.add("unlike");
                    socket_interact.send(JSON.stringify({
                        'user' : ThisUser.id,
                        'post_id' : button.id,
                        'active' : 'unlike'
                    }));
                    value_like=false;
                }
                else{
                    button.classList.remove("unlike");
                    button.classList.add("like");
                    socket_interact.send(JSON.stringify({
                        'user' : ThisUser.id,
                        'post_id' : button.id,
                        'active' : 'like'
                    }));
                    socket_noti.send(JSON.stringify({
                        'user' : ThisUser.id,
                        'to_post_id' : button.id,
                        'text' : 'like'
                    }));
                    value_like=true;
                }
                
            })
            break;
    
        case false:
            var value_unlike=true;
            button.addEventListener('click', () => {
                if (value_unlike) {
                    button.classList.remove("unlike");
                    button.classList.add("like");
                    socket_interact.send(JSON.stringify({
                        'user' : ThisUser.id,
                        'post_id' : button.id,
                        'active' : 'like'
                    }));
                    socket_noti.send(JSON.stringify({
                        'user' : ThisUser.id,
                        'to_post_id' : button.id,
                        'text' : 'like'
                    }));
                    value_unlike=false;
                }
                else{
                    button.classList.remove("like");
                    button.classList.add("unlike");
                    socket_interact.send(JSON.stringify({
                        'user' : ThisUser.id,
                        'post_id' : button.id,
                        'active' : 'unlike'
                    }));
                    value_unlike=true;
                }
                
            })
    }
})


// =========function receive like===========
function like_post(data) {
    PostLikeCount.forEach(item => {
        if (item.id == data.post_id) {
            item.innerHTML = parseInt(item.innerHTML) + 1;
        }
    });
    LikeCountFunct();
}
function unlike_post(data) {
    PostLikeCount.forEach(item => {
        if (item.id == data.post_id) {
            item.innerHTML = parseInt(item.innerHTML) - 1;
        }
    });
    LikeCountFunct();
}



// =============================comment============================
InputCmtForm.forEach(input => {
    input.onkeyup = function(e) {
        if (e.keyCode == 13) {
            SubmitCmtForm.forEach(submit => {
                if (input.id == submit.id) {
                    submit.click();
                }
            })
        }
    }
})

function CmtCountFunct() {
    PostCmtCount.forEach(item => {
        if (parseInt(item.innerHTML) == 0) {
            item.style.display = "none";
        }
        else{
            item.style.display = "block";
        }
    })
}
CmtCountFunct();

// ==========send comment===========
SubmitCmtForm.forEach(submit => {
    submit.onclick = function() {
        InputCmtForm.forEach(input => {
            if (submit.id==input.id) {
                if (input.value.length != 0) {
                    socket_interact.send(JSON.stringify({
                        'user' : ThisUser.id,
                        'post_id' : submit.id,
                        'active' : 'comment',
                        'text' : input.value
                    }));
                    socket_noti.send(JSON.stringify({
                        'user' : ThisUser.id,
                        'to_post_id' : submit.id,
                        'text' : 'comment'
                    }));
                }
                input.value = "";
            }
        })
    }
})

RemoveCmt.forEach(remove => {
    remove.addEventListener('click', () => {
        var id = remove.getAttribute('data-id');
        socket_interact.send(JSON.stringify({
            'user' : ThisUser.id,
            'post_id' : id,
            'cmt_id' : remove.id,
            'active' : 'remove_comment',
        }));
    })
})

// =========function receive comment===========
function comment_post(data) {
    CmtCount.forEach(count => {
        if (count.id==data.post_id) {
            var value = count.innerHTML.split(" ")[0];
            num = parseInt(value) + 1;
            count.innerHTML = num + " comment";
        }
        CmtCountFunct();
    })
    CmtCard.forEach(card => {
        if (card.id == data.post_id) {
            if (ThisUser.id==data.user) {
                card.innerHTML = (
                    '<div class="cmt_item" id="' +
                    data.cmt_id +
                    '"><div class="profile-picture"><img src="' +
                    data.user_img +
                    '"></div><div class="context"><strong>' +
                    data.full_name +
                    '</strong><p>' +
                    data.text +
                    '</p></div><div class="edit"><i class="fa-solid fa-ellipsis"></i>' +
                    '<div class="function"><button class="remove_cmt_post" id="' +
                    data.cmt_id +
                    '" data-id="' +
                    data.post_id + 
                    '">Remove</buton></div></div></div>'
                ) + card.innerHTML;
            }
            else{
                card.innerHTML = (
                    '<div class="cmt_item" id="' +
                    data.cmt_id +
                    '"><div class="profile-picture"><img src="' +
                    data.user_img +
                    '"></div><div class="context"><strong>' +
                    data.full_name +
                    '</strong><p>' +
                    data.text +
                    '</p></div></div>'
                ) + card.innerHTML;
            }
        }
    })
}

function remove_comment_post(data) {
    CmtCount.forEach(count => {
        if (count.id==data.post_id) {
            var value = count.innerHTML.split(" ")[0];
            num = parseInt(value) - 1;
            count.innerHTML = num + " comment";
        }
        CmtCountFunct();
    })
    CmtItem.forEach(cmt => {
        if (cmt.id == data.cmt_id) {
            cmt.style.display = "none";
        }
    })
}