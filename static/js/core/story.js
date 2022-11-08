const UserItem = document.querySelectorAll('.story-user');
const StoryItem = document.querySelectorAll('.content');
const clear = document.querySelector('#clear');
const input_file = document.querySelector('#image');

const ChatPopupItem = document.querySelectorAll('.message');
const ChatItem = document.querySelectorAll('.chat_win');
const CloseChat = document.querySelectorAll('.close_win');

const UserchangeActive = () => {
    UserItem.forEach(item => {
        item.classList.remove('active');
    })
}
UserItem.forEach(item => {
    item.addEventListener('click', () => {
        UserchangeActive();
        item.classList.add('active');
        var id = item.getAttribute('data-id');
        StoryItem.forEach(story_item => {
            if(story_item.id == id){
                story_item.style.display = "block";
            }
            else{
                story_item.style.display = "none";
            }
        })
    })
})

clear.addEventListener('click', () => {
    input_file.value = "";
    document.getElementById('blah').src = document.getElementById('background').src;
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