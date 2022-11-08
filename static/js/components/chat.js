const label_input_chat = document.querySelectorAll('#input_photo_chat');
const image_upload_arena = document.querySelectorAll('.image_upload');
const label_clear_chat = document.querySelectorAll('#clear_photo_chat');
const store_image_upload = document.querySelectorAll('.store_image_upload');

const input_text = document.querySelectorAll('.input_text_chat');
const WinContentList = document.querySelectorAll('.chat_win .win_content');


label_input_chat.forEach(item => {
    item.addEventListener('click', () => {
        var id = item.getAttribute('data-id');
        image_upload_arena.forEach(arena => {
            if(arena.id == id){
                arena.style.display = "block";

                label_clear_chat.forEach(clear => {
                    var clear_id = clear.getAttribute('data-id');
                    clear.addEventListener('click', () => {
                        if(clear_id == arena.id){
                            arena.style.display = "none";
                            store_image_upload.forEach(store => {
                                store.src = document.getElementById('background_chat').src
                            })
                        }
                    })
                })
            }
            else{
                arena.style.display = "none";
            }
        })
    })
    
})


input_text.forEach(input => {
    input.onkeyup = function(e) {
        if (e.keyCode == 13) {
            if (input.value.length == 0 ) return;
            socket_chat.send(JSON.stringify({
                "to_user" : input.id,
                "text" : input.value,
            }));
            input.value = "";
        }
    }
})


function scroll_mess() {
    WinContentList.forEach(win => {
        win.scrollTop = win.scrollHeight;
    })
}

function update_chat(data) {
    ChatItem.forEach(item => {
        if (item.id != ThisUser.id) {
            if (item.id==data.user) {
                item.style.display = "flex";

                CloseChat.forEach(close_item => {
                    close_item.addEventListener('click', () => {
                        var close_id = close_item.getAttribute('id');
                        if(close_id == item.id){
                            item.style.display = "none";
                        }
                    })
                })
            }
        }
    })
    if (data.user==ThisUser.id) {
        WinContentList.forEach(win => {
            if (data.to_user==win.id) {
                win.innerHTML += '<div class="msg_container message_send"><div class="msg-box"><p>'
                + data.text
                + '</p></div></div>';
            }
        })
    }
    if (data.to_user==ThisUser.id) {
        WinContentList.forEach(win => {
            if (data.user==win.id) {
                win.innerHTML += '<div class="msg_container message_receive"><div class="msg-box"><p>'
                + data.text
                + '</p></div></div>';
            }
        })
    }
    scroll_mess();
}