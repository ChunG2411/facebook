const edit_profile = document.querySelector('.edit-profile-button');
const card_profile = document.querySelector('.edit-profile-card');

const ChatPopupItem = document.querySelectorAll('.message');
const ChatItem = document.querySelectorAll('.chat_win');
const CloseChat = document.querySelectorAll('.close_win');


//edit profile
edit_profile.addEventListener('click', () => {
    card_profile.style.display = 'grid';
})
card_profile.addEventListener('click', (e) => {
    if(e.target.classList.contains('edit-profile-card')){
        card_profile.style.display = 'none';
    }
})



//chat
const ChatItem_each = (id) => {
    ChatItem.forEach(chat_item => {
        if(chat_item.id == id){
            chat_item.style.display = "flex";
            scroll_mess();
            socket_chat.send(JSON.stringify({
                "to_user" : chat_item.id,
            }));
            DisplayNewMess.forEach(display => {
                display.innerHTML = "Click to chat";
            });

            CloseChat.forEach(close_item => {
                close_item.addEventListener('click', () => {
                    var close_id = close_item.getAttribute('id');
                    if(close_id == id){
                        chat_item.style.display = "none";
                    }
                })
            })
        }
        else{
            chat_item.style.display = "none";
        }
    })
}

ChatPopupItem.forEach(item => {
    item.addEventListener('click', () => {
        var id = item.getAttribute('data-id');
        ChatItem_each(id);
    })
})


// socket
function compare(params) {}