// dark mode & lang
var j=jQuery.noConflict();
window.onload=function(){var e=document.getElementById("profile-more-submenu"),o=document.getElementById("profile-more-actions");document.onclick=function(t){"profile-more-submenu"===t.target.id?t.preventDefault():"profile-more-actions"===t.target.id?(e.classList.toggle("open"),o.classList.toggle("active")):(e.classList.remove("open"),o.classList.remove("active"))}},j(document).ready(function(){autosize(document.querySelectorAll("textarea"));document.getElementById("switch-shadow");var e=document.getElementById("mode-text");j("#switch-shadow").change(function(){this.checked?(e.innerHTML="<?php echo ucwords_tr($darkmode); ?>",document.getElementsByTagName("BODY")[0].classList.add("dark"),document.getElementById("logo3").srcset="<?php echo get_stylesheet_directory_uri(); ?>/assets/img/header/sosyorol-logo3-dark.webp",document.getElementById("logo2").srcset="<?php echo get_stylesheet_directory_uri(); ?>/assets/img/header/sosyorol-logo1-dark.jpg",document.getElementById("logo1").src="<?php echo get_stylesheet_directory_uri(); ?>/assets/img/header/sosyorol-logo1-dark.jpg",jQuery.ajax({type:"POST",url:"https://www.sosyorol.com/user-preferences/",async:!0,data:{uid:"<?php echo $userID; ?>",sel:"dark",op:"mode"},success:function(e){location.reload()},error:function(e,o,t){}})):(e.innerHTML="<?php echo ucwords_tr($lightmode); ?>",document.getElementsByTagName("BODY")[0].classList.remove("dark"),document.getElementById("logo3").srcset="<?php echo get_stylesheet_directory_uri(); ?>/assets/img/header/sosyorol-logo3.webp",document.getElementById("logo2").srcset="<?php echo get_stylesheet_directory_uri(); ?>/assets/img/header/sosyorol-logo1.jpg",document.getElementById("logo1").src="<?php echo get_stylesheet_directory_uri(); ?>/assets/img/header/sosyorol-logo1.jpg",jQuery.ajax({type:"POST",url:"https://www.sosyorol.com/user-preferences/",async:!0,data:{uid:"<?php echo $userID; ?>",sel:"light",op:"mode"},success:function(e){},error:function(e,o,t){}}))})});
    
// menus
var scrollDuration = 600,
    itemsLength = 8,
        itemsLength2 = 10,
        itemSize = 222,
        itemSize2 = 180,
        paddleMargin = 0;
    
    function getMenuWrapperSize(e) {
        return j("#" + e).outerWidth()
    }
    var menuWrapperSize = getMenuWrapperSize("menu-wrapper"),
        menuWrapperSize2 = getMenuWrapperSize("menu-wrapper2");
    j(window).on("resize", function() {
        menuWrapperSize = getMenuWrapperSize("menu-wrapper"), menuWrapperSize2 = getMenuWrapperSize("menu-wrapper2")
    });
    var menuVisibleSize = menuWrapperSize,
        menuVisibleSize2 = menuWrapperSize2;
    
    function getMenuSize(e, n) {
        return e * n
    }
    var menuSize = getMenuSize(itemsLength, itemSize),
        menuInvisibleSize = menuSize - menuWrapperSize,
        menuSize2 = getMenuSize(itemsLength2, itemSize2),
        menuInvisibleSize2 = menuSize2 - menuWrapperSize2;
    
    function getMenuPosition(e) {
        return j("#" + e).scrollLeft()
    }
    
    function menuScroll(e, n, i, t) {
        if (1 == t) {
            menuInvisibleSize = menuSize - menuWrapperSize;
            var r = getMenuPosition(i);
            r <= paddleMargin ? (document.getElementById(e).classList.add("hidden"), document.getElementById(n).classList.remove("hidden")) : r < 1319 ? (document.getElementById(e).classList.remove("hidden"), document.getElementById(n).classList.remove("hidden")) : r >= 1319 && (document.getElementById(e).classList.remove("hidden"), document.getElementById(n).classList.add("hidden"))
        } else if (2 == t) {
            menuInvisibleSize2 = menuSize2 - menuWrapperSize2;
            r = getMenuPosition(i);
            r <= paddleMargin ? (document.getElementById(e).classList.add("hidden"), document.getElementById(n).classList.remove("hidden")) : r < 1188 ? (document.getElementById(e).classList.remove("hidden"), document.getElementById(n).classList.remove("hidden")) : r >= 1188 && (document.getElementById(e).classList.remove("hidden"), document.getElementById(n).classList.add("hidden"))
        }
    }
    
    function scrollToLeft(e) {
        var n = getMenuPosition(e);
        1319 - n > 792 ? j("#" + e).animate({
            scrollLeft: n + 792
        }, scrollDuration) : j("#" + e).animate({
            scrollLeft: 1319
        }, scrollDuration)
    }
    
    function scrollToRight(e) {
        var n = getMenuPosition(e);
        n - 792 > 0 ? j("#" + e).animate({
            scrollLeft: n - 792
        }, scrollDuration) : j("#" + e).animate({
            scrollLeft: 0
        }, scrollDuration)
    }
    
    // upvote & downvote & comment-editor
    function upvote(e, csrf) {
        document.getElementById("upvote" + e).classList.contains("active") ? (document.getElementById("upvote" + e).classList.remove("active"), document.getElementById("vote" + e).classList.add("animatedown"), document.getElementById("vote" + e).classList.remove("red"), document.getElementById("vote" + e).classList.remove("main-color"), document.getElementById("vote" + e).innerHTML = (parseInt(document.getElementById("vote" + e).innerHTML) - 1).toString(), setTimeout(function() {
            document.getElementById("vote" + e).classList.remove("animatedown")
        }, 300)) : (document.getElementById("vote" + e).classList.add("animateup"), document.getElementById("upvote" + e).classList.add("active"), document.getElementById("vote" + e).classList.remove("red"), document.getElementById("vote" + e).classList.add("main-color"), document.getElementById("downvote" + e).classList.contains("active") ? (document.getElementById("downvote" + e).classList.remove("active"), document.getElementById("vote" + e).innerHTML = (parseInt(document.getElementById("vote" + e).innerHTML) + 2).toString()) : document.getElementById("vote" + e).innerHTML = (parseInt(document.getElementById("vote" + e).innerHTML) + 1).toString(), setTimeout(function() {
            document.getElementById("vote" + e).classList.remove("animateup")
        }, 300))
        if (document.getElementById("upvote" + e).classList.contains("active")) {
            j.ajax({
                url:"postrating/",
                type : "POST", // http method
                data : {csrfmiddlewaretoken: csrf, redirect: window.location.href, post_id : e, opinion : "like", operation: "add"}, // data sent with the post request
                // handle a successful response
                success : function(json) {
                     // log the returned json to the console
                    console.log("success"); // another sanity check
                }
            });
        }else{
            j.ajax({
                url:"postrating/",
                type : "POST", // http method
                data : {csrfmiddlewaretoken: csrf, redirect: window.location.href, post_id : e, opinion : "like", operation: "remove"}, // data sent with the post request
                // handle a successful response
                success : function(json) {
                     // log the returned json to the console
                    console.log("success"); // another sanity check
                }
            });
        }
    }
    
    function downvote(e,csrf) {
        document.getElementById("downvote" + e).classList.contains("active") ? (document.getElementById("downvote" + e).classList.remove("active"), document.getElementById("vote" + e).classList.add("animateup"),  document.getElementById("vote" + e).classList.remove("red"), document.getElementById("vote" + e).classList.remove("main-color"), document.getElementById("vote" + e).innerHTML = (parseInt(document.getElementById("vote" + e).innerHTML) + 1).toString(), setTimeout(function() {
            document.getElementById("vote" + e).classList.remove("animateup")
        }, 300)) : (document.getElementById("vote" + e).classList.add("animatedown"), document.getElementById("downvote" + e).classList.add("active"), document.getElementById("vote" + e).classList.add("red"), document.getElementById("vote" + e).classList.remove("main-color"), document.getElementById("upvote" + e).classList.contains("active") ? (document.getElementById("upvote" + e).classList.remove("active"), document.getElementById("vote" + e).innerHTML = (parseInt(document.getElementById("vote" + e).innerHTML) - 2).toString()) : document.getElementById("vote" + e).innerHTML = (parseInt(document.getElementById("vote" + e).innerHTML) - 1).toString(), setTimeout(function() {
            document.getElementById("vote" + e).classList.remove("animatedown")
        }, 300))
        if (document.getElementById("downvote" + e).classList.contains("active")) {
            j.ajax({
                url:"postrating/",
                type : "POST", // http method
                data : {csrfmiddlewaretoken: csrf, redirect: window.location.href, post_id : e, opinion : "dislike", operation: "add"}, // data sent with the post request
                // handle a successful response
                success : function(json) {
                     // log the returned json to the console
                    console.log("success"); // another sanity check
                }
            });
        }else{
            j.ajax({
                url:"postrating/",
                type : "POST", // http method
                data : {csrfmiddlewaretoken: csrf, redirect: window.location.href, post_id : e, opinion : "dislike", operation: "remove"}, // data sent with the post request
                // handle a successful response
                success : function(json) {
                     // log the returned json to the console
                    console.log("success"); // another sanity check
                }
            });
        }
    }
    
    function commentEditorChange(e) {
        var t = document.getElementById("comment-editor" + e).value,
            n = document.getElementById("comment-send-btn" + e);
        "" == t ? n.classList.contains("active") && n.classList.remove("active") : n.classList.contains("active") || n.classList.add("active")
    }