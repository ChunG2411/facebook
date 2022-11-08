const Tab = document.querySelectorAll('.tab_head .tab');
const ContentReceive = document.querySelector('.content_receive');
const ContentSend = document.querySelector('.content_send');
const ContentFriend = document.querySelector('.content_friend');

const ChatPopupItem = document.querySelectorAll('.message');
const ChatItem = document.querySelectorAll('.chat_win');
const CloseChat = document.querySelectorAll('.close_win');


const changeActiveTab = () => {
    Tab.forEach(tab => {
        tab.classList.remove('active');
    })
}

Tab.forEach(tab => {
    tab.addEventListener('click', () => {
        changeActiveTab();
        tab.classList.add('active');

        if (tab.id == "receive") {
            ContentReceive.style.display = "block";
            ContentSend.style.display = "none";
            ContentFriend.style.display = "none";
        }
        else if (tab.id == "send") {
            ContentReceive.style.display = "none";
            ContentSend.style.display = "block";
            ContentFriend.style.display = "none";
        }
        else if (tab.id == "friend") {
            ContentReceive.style.display = "none";
            ContentSend.style.display = "none";
            ContentFriend.style.display = "block";
        }
    })
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