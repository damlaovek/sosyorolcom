function updateTextareaCounter(elem,cId, maxVal){
    var len = elem.value.length;
    document.getElementById(cId).innerHTML = len+"/"+maxVal;
}
function selectLanguage() {
    document.getElementById('lang-popup').classList.toggle('hidden');
}
function updateLanguage(e, uid) {
    jQuery.ajax({
        type: "POST",
        url: "/updatelanguage/",
        async: !0,
        data: {
            uid: uid,
            lang: e,
            op: "lang"
        },
        success: function(e) {
            window.location.href = window.location.href;
        },
        error: function(e, o, t) {}
    })
}
function showHide(elemId){
    var elem = document.getElementById(elemId);
    elem.classList.toggle('hidden');
}

function showHide2(elemId){
    var elem = document.getElementById(elemId);
    if(elem.style.display == "none"){
        elem.style.display = "block";
    }else{
        elem.style.display = "none";
    }
}

function setCookie(cname, cvalue, exsecs) {
    var d = new Date();
    d.setTime(d.getTime() + (exsecs*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
}

function checkViewsCookie(){
    var url = window.location.href;
    if(getCookie(url) == url){
        // Already viewed do nothing
    }else{
        // set view cookie
        setCookie(url, url, 300);
        // TODO: Increment view count
    }
}