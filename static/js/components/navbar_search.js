const MenuItems = document.querySelectorAll('.menu-item');
const ProfileButton = document.querySelector('.navbar .profile');

const popup = document.querySelector('.popup');
const search_popup = document.querySelector('.search-popup');
const notifications_popup = document.querySelector('.notifications-popup');
const chats_popup = document.querySelector('.chats-popup');
const profile_popup = document.querySelector('.profile-popup');

const exit_search = document.querySelector('#exit-search');
const exit_noti = document.querySelector('#exit-noti');
const exit_chat = document.querySelector('#exit-chat');

const message_search = document.querySelector('#messenger-search');
const message = chats_popup.querySelectorAll('.message');


//active item navbar
const changeActive = () => {
    MenuItems.forEach(item => {
        item.classList.remove('active');
    })
}
const search = () => {
    MenuItems[1].classList.add('active');
    popup.style.display = 'block';
    search_popup.style.display = 'block';
}

check_click_profile = true;
ProfileButton.addEventListener('click', () => {
    if (check_click_profile) {
        popup.style.display = 'block';
        profile_popup.style.display = "block";
        chats_popup.style.display = 'none';
        notifications_popup.style.display = 'none';
        search_popup.style.display = 'none';

        changeActive();
        check_click_profile = false;
    }
    else{
        popup.style.display = 'none';
        profile_popup.style.display = "none";

        changeActive();
        MenuItems[0].classList.add('active');
        check_click_profile = true;
    }
})

MenuItems.forEach(item => {
    changeActive();
    search();

    item.addEventListener('click', () => {
        changeActive();
        item.classList.add('active');
        
        if(item.id == 'notifications'){
            document.querySelector('#notifications .count').style.display = 'none';
            popup.style.display = 'block';
            notifications_popup.style.display = 'block';
            chats_popup.style.display = 'none';
            search_popup.style.display = 'none';
            profile_popup.style.display = "none";

            // socket noti
            socket_noti.send(JSON.stringify({
                'user' : ThisUser.id,
                'text' : 'read_all'
            }));
            
        } else if(item.id == 'messenger'){
            document.querySelector('#messenger .count').style.display = 'none';
            popup.style.display = 'block';
            chats_popup.style.display = 'block';
            notifications_popup.style.display = 'none';
            search_popup.style.display = 'none';
            profile_popup.style.display = "none";

        } else{
            popup.style.display = 'block';
            chats_popup.style.display = 'none';
            notifications_popup.style.display = 'none';
            search_popup.style.display = 'block';
            profile_popup.style.display = "none";

        }
    })
})

//close popup
exit_search.addEventListener('click', () => {
    popup.style.display = 'none';
    search_popup.style.display = 'none';
    changeActive();
    search();
})
exit_noti.addEventListener('click', () => {
    popup.style.display = 'none';
    notifications_popup.style.display = 'none';
    changeActive();
    search();
})
exit_chat.addEventListener('click', () => {
    popup.style.display = 'none';
    chats_popup.style.display = 'none';
    changeActive();
    search();
})

//search messenger
const search_message = () => {
    const val = message_search.value.toLowerCase();
    message.forEach(user => {
        let name = user.querySelector('h4').textContent.toLowerCase();
        if(name.indexOf(val) != -1){
            user.style.display = 'flex';
        } else{
            user.style.display = 'none';
        }
    })
}
message_search.addEventListener('keyup', search_message);