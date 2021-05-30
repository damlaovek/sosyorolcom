function joinCommunity(elem, community_id, txt){
    jQuery.ajax({
        type: "POST",
        url: "/followunfollowcommunity",
        async: !0,
        data: {
            community_id: community_id,
            op: "follow",
        },
        success: function(e) {
            current_txt = elem.innerText;
            elem.innerText = txt;
            elem.onclick = function(){return unfollowCommunity(elem, community_id, current_txt)}
        },
        error: function(e, o, t) {}
    })
}

function unfollowCommunity(elem, community_id, txt){
    jQuery.ajax({
        type: "POST",
        url: "/followunfollowcommunity",
        async: !0,
        data: {
            community_id: community_id,
            op: "unfollow",
        },
        success: function(e) {
            current_txt = elem.innerText;
            elem.innerText = txt;
            elem.onclick = function(){return joinCommunity(elem, community_id, current_txt)}
        },
        error: function(e, o, t) {}
    })
}