const NotiContent = document.querySelector('.notifications-popup .content');
const CountNoti = document.querySelector('#notifications .count');
const Notifriend = document.querySelectorAll('.noti_friend');
const confirm_friend = document.querySelectorAll('.action .confirm');
const decline_friend = document.querySelectorAll('.action .decline');


function noti(data) {
    if (CountNoti.id == data.to_user) {
        if (data.user != ThisUser.id) {

            CountNoti.style.display = "inline";
            if (data.content != "send you friend request") {
                NotiContent.innerHTML = '<div style="background:rgb(231, 231, 231);"><div class="profile-picture"><img src="'
                + data.user_img
                + '"></div><div class="body-content"><p><b> '
                + data.user_fullname
                + ' </b> '
                + data.content
                + '</p><small id="create_on">'
                + data.timestamp
                + '</small></div></div>'
                + NotiContent.innerHTML;
            }
            else{
                NotiContent.innerHTML = '<div class="noti_friend" style="background:rgb(231, 231, 231);" id="'
                + data.user
                + '"><div class="profile-picture"><img src="'
                + data.user_img
                + '"></div><div class="body-content"><p><b>'
                + data.user_fullname
                + ' </b>'
                + data.content
                + '</p><small id="create_on">'
                + data.timestamp
                + '</small><div class="action"><a href=""><button class="btn confirm">Detail</button></a>'
                + '</div></div></div>'
                + NotiContent.innerHTML;
            }
        }
    }
    else{
        CountNoti.style.display = "none";
    }
}


confirm_friend.forEach(item => {
    item.addEventListener('click', () => {
        socket_friend.send(JSON.stringify({
            'user' : item.id,
            'active' : 'confirm'
        }));
        Notifriend.forEach(noti => {
            if (noti.id == item.id) {
                noti.style.display = "none";
            }
        })
    })
})

decline_friend.forEach(item => {
    item.addEventListener('click', () => {
        socket_friend.send(JSON.stringify({
            'user' : item.id,
            'active' : 'decline'
        }));
        Notifriend.forEach(noti => {
            if (noti.id == item.id) {
                noti.style.display = "none";
            }
        })
    })
})

