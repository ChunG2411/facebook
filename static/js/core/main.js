const post = document.querySelector('.post');
const post_card = document.querySelector('#post-create');

const input_file = document.querySelector('#image');
const label_input = document.querySelector('#input_photo');
const label_clear = document.querySelector('#clear');

const ContactItem = document.querySelectorAll('.contact-user');
const ChatPopupItem = document.querySelectorAll('.message');
const ChatItem = document.querySelectorAll('.chat_win');
const CloseChat = document.querySelectorAll('.close_win');
const DisplayNewMess = document.querySelectorAll('.display_new-mess');

const StoryFeed = document.querySelector('.feeds .stories');
const ButtonNextStory = document.querySelector('.scroll_next_story');
const ButtonPreStory = document.querySelector('.scroll_pre_story');

const StatusIcon = document.querySelectorAll('.status-icon');


//post create
post.addEventListener('click', () => {
    post_card.style.display = 'grid';
})
post_card.addEventListener('click', (e) => {
    if(e.target.classList.contains('post-create')){
        post_card.style.display = 'none';
    }
})

label_clear.addEventListener('click', () => {
    input_file.value = "";
    document.getElementById('blah').src = document.getElementById('background').src
    document.getElementById('blah').style.display = "none";
})
label_input.addEventListener('click', () => {
    document.getElementById('blah').style.display = "block";
})

//chat
const ChatItem_each = (id, item) => {
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

ContactItem.forEach(item => {
    item.addEventListener('click', () => {
        var id = item.getAttribute('data-id');
        item.classList.add('active');
        ChatItem_each(id, item);
    })
})

ChatPopupItem.forEach(item => {
    item.addEventListener('click', () => {
        var id = item.getAttribute('data-id');
        ChatItem_each(id);
    })
})

// scrollbar stories
ButtonNextStory.addEventListener('click', () => {
    sideScroll(StoryFeed,'right',25,100,10);

    ButtonPreStory.style.display="grid";
    if(StoryFeed.scrollWidth - StoryFeed.scrollLeft - StoryFeed.offsetWidth<100){
        ButtonNextStory.style.display="none";
    }
})
ButtonPreStory.addEventListener('click', () => {
    sideScroll(StoryFeed,'left',25,100,10);

    ButtonNextStory.style.display="grid";
    if (StoryFeed.scrollLeft<100) {
        ButtonPreStory.style.display="none";
    }
})
if (StoryFeed.scrollWidth > StoryFeed.clientWidth) {
    ButtonNextStory.style.display="grid";
}

function sideScroll(element,direction,speed,distance,step){
    scrollAmount = 0;
    var slideTimer = setInterval(function(){
        if(direction == 'left'){
            element.scrollLeft -= step;
        } else {
            element.scrollLeft += step;
        }
        scrollAmount += step;
        
        if(scrollAmount >= distance){
            window.clearInterval(slideTimer);
        }
    }, speed);
}


// socket user status
function compare(data) {
    StatusIcon.forEach(item => {
        if (data.includes(item.id)) {
            item.style.color = "rgb(0, 211, 0)";
        }
        else{
            item.style.color = "gray";
        }
    })
}

