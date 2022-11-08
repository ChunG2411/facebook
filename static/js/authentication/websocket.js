const socket_interact = new WebSocket('ws://127.0.0.1:8000/interact/');
const socket_noti = new WebSocket('ws://127.0.0.1:8000/noti/');
const socket_friend = new WebSocket('ws://127.0.0.1:8000/friend/');
const socket_chat = new WebSocket('ws://127.0.0.1:8000/chat/');


// socket interact
function connect_interact() {
    socket_interact.onopen = function(){
        console.log("Websocket interact is connected");
    }
    socket_interact.onclose = function(){
        console.log("Websocket interact is disconnected");
        setTimeout(function() {
            console.log("Websocket interact reconnecting...");
            connect_interact();
        }, 2000);
    }
    socket_interact.onmessage = function(e){
        var data = JSON.parse(e.data);

        switch (data.type) {
            case "list_user_online":
                compare(data.list);
                break;
            case "like_post":
                like_post(data);
                break;
            case "unlike_post":
                unlike_post(data);
                break;
            case "comment_post":
                comment_post(data);
                break;
            case "rmv_cmt":
                remove_comment_post(data);
                break;
        }
    }
}
connect_interact();


// socket noti
function connect_noti() {
    socket_noti.onopen = function(){
        console.log("Websocket noti is connected");
    }
    socket_noti.onclose = function(){
        console.log("Websocket noti is disconnected");
        setInterval(function() {
            console.log("Websocket noti reconnecting...");
            connect_noti();
        }, 2000);
    }
    socket_noti.onmessage = function(e){
        var data = JSON.parse(e.data);
        
        switch (data.type) {
            case "noti_like":
                noti(data);
                break;
            case "noti_comment":
                noti(data);
                break;
            case "noti_friend":
                noti(data);
                break;
        }
    }
}
connect_noti();


// socket friend
function connect_friend() {
    socket_friend.onopen = function(){
        console.log("Websocket friend is connected");
    }
    socket_friend.onclose = function(){
        console.log("Websocket friend is disconnected");
        setTimeout(function() {
            console.log("Websocket friend reconnecting...");
            connect_friend();
        }, 2000);
    }
    socket_friend.onmessage = function(e){
        var data = JSON.parse(e.data);
    }
}
connect_friend();


// socket chat
function connect_chat() {
    socket_chat.onopen = function(){
        console.log("Websocket chat is connected");
    }
    socket_chat.onclose = function(){
        console.log("Websocket chat is disconnected");
        setTimeout(function() {
            console.log("Websocket chat reconnecting...");
            connect_chat();
        }, 2000);
    }
    socket_chat.onmessage = function(e){
        var data = JSON.parse(e.data);

        switch (data.type) {
            case "message_text":
                update_chat(data);        
                break;
        
        }
    }
}
connect_chat();