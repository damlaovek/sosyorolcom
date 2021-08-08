function follow(elem, followerId, followingId, txt, current="-1", profile="-1"){
    data = {
        "op": "follow",
        "followerId": followerId,
        "followingId": followingId
    }
    jQuery.ajax({
        type: "GET",
        url:"/followunfollowuser/",
        data: data,
        success: function(response) {
            displayAlert(response.content);
            var followtxt = elem.innerHTML.replace('<span class="p115">', "").replace('</span>', "");
            elem.innerHTML = '<span class="p115">'+txt+'</span>';
            elem.style.backgroundColor = "var(--main-color)";
            elem.style.color = "white";
            elem.onclick = function() { return unfollow(elem, followerId, followingId, followtxt, current, profile);};
            if(current == followerId){
                if(profile == followingId){
                    var num_follower = parseInt(document.getElementById("num_follower").innerHTML);
                    document.getElementById("num_follower").innerHTML = (num_follower + 1).toString();
                }else if(profile == current){
                    var num_following = parseInt(document.getElementById("num_following").innerHTML);
                    document.getElementById("num_following").innerHTML = (num_following + 1).toString();
                }
            }
        }
    });
    return false;
}
function unfollow(elem, followerId, followingId, txt, current="-1", profile="-1"){
    data = {
        "op": "unfollow",
        "followerId": followerId,
        "followingId": followingId
    }
    jQuery.ajax({
        type: "GET",
        url:"/followunfollowuser/",
        data: data,
        success: function(response) {
            displayAlert(response.content);
            var followingtxt = elem.innerHTML.replace('<span class="p115">', "").replace('</span>', "");
            elem.innerHTML = '<span class="p115">'+txt+'</span>';
            elem.style.backgroundColor = "var(--main-color-alpha)";
            elem.style.color = "var(--main-color)";
            elem.onclick = function() { return follow(elem, followerId, followingId, followingtxt, current, profile); };
            if(current == followerId){
                if(profile == followingId){
                    var num_follower = parseInt(document.getElementById("num_follower").innerHTML);
                    document.getElementById("num_follower").innerHTML = (num_follower - 1).toString();
                }else if(profile == current){
                    var num_following = parseInt(document.getElementById("num_following").innerHTML);
                    document.getElementById("num_following").innerHTML = (num_following - 1).toString();
                }
            }
        }
    });
    return false;
}