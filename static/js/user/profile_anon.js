const ContactItem = document.querySelector('.mess');
const ChatPopupItem = document.querySelectorAll('.message');
const ChatItem = document.querySelectorAll('.chat_win');
const CloseChat = document.querySelectorAll('.close_win');

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
ContactItem.addEventListener('click', () => {
    var id = ContactItem.getAttribute('data-id');
    ChatItem_each(id);
})

ChatPopupItem.forEach(item => {
    item.addEventListener('click', () => {
        var id = item.getAttribute('data-id');
        ChatItem_each(id);
    })
})


function compare(params) {}