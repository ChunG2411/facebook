const RemoveFriend = document.querySelector('.right .remove');
const CancerFriend = document.querySelector('.right .cancer');
const ConfirmFriend = document.querySelector('.right .confirm');
const DeclineFriend = document.querySelector('.right .decline');
const AddFriend = document.querySelector('.right .add');

const Right = document.querySelector('.avatar .right');

RemoveFriend.addEventListener('click', () => {
    RemoveFriend.style.display = "none";
    AddFriend.style.display = "block";

    socket_friend.send(JSON.stringify({
        'user' : Right.id,
        'active' : 'remove'
    }));
})

AddFriend.addEventListener('click', () => {
    AddFriend.style.display = "none";
    CancerFriend.style.display = "block";

    socket_friend.send(JSON.stringify({
        'user' : Right.id,
        'active' : 'add'
    }));
    socket_noti.send(JSON.stringify({
        'user' : ThisUser.id,
        'to_user' : Right.id,
        'text' : 'add'
    }));
})

CancerFriend.addEventListener('click', () => {
    CancerFriend.style.display = "none";
    AddFriend.style.display = "block";

    socket_friend.send(JSON.stringify({
        'user' : Right.id,
        'active' : 'cancer'
    }));
})

ConfirmFriend.addEventListener('click', () => {
    ConfirmFriend.style.display = "none";
    DeclineFriend.style.display = "none";
    RemoveFriend.style.display = "block";

    socket_friend.send(JSON.stringify({
        'user' : Right.id,
        'active' : 'confirm'
    }));
})

DeclineFriend.addEventListener('click', () => {
    ConfirmFriend.style.display = "none";
    DeclineFriend.style.display = "none";
    AddFriend.style.display = "block";

    socket_friend.send(JSON.stringify({
        'user' : Right.id,
        'active' : 'decline'
    }));
})


