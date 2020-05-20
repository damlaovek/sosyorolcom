function deleteElementById(elemId){document.getElementById(elemId).remove();}
function displayAlert(alertTxt){
    if (j( "#alert-box-container" ).length ) {
        j( "#alert-box-container" ).remove();
    }    
    var alertboxcontainer = document.createElement('div');
    alertboxcontainer.setAttribute("class", "alert-box-container");
    alertboxcontainer.setAttribute("id", "alert-box-container");
    var alertbox = document.createElement('div');
    alertbox.setAttribute("class", "alert-box noselect");
    alertbox.setAttribute("id", "alert-box");
    alertbox.setAttribute("onmouseover", "alertBoxHover()");
    alertbox.setAttribute("onmouseleave", "alertBoxHoverOut()");
    alertbox.innerHTML = alertTxt;
    alertboxcontainer.appendChild(alertbox);
    document.body.appendChild(alertboxcontainer);
    var close = document.createElement('div');
    close.setAttribute("id", "alert-box-close");
    close.setAttribute("class", "hand");
    close.setAttribute("onmouseover", "alertBoxHover()");
    close.setAttribute("onmouseleave", "alertBoxHoverOut()");
    close.setAttribute("onclick", "document.getElementById('alert-box-container').classList.remove('in')");
    alertbox.appendChild(close);
    setTimeout(function(){ alertboxcontainer.classList.add("in");}, 300);
    setTimeout(function(){
        var classList = document.getElementById('alert-box').classList;
        if(classList.contains('hover')){
            alertbox.setAttribute("onmouseleave", "document.getElementById('alert-box-container').classList.remove('in')");
        }else{
             document.getElementById('alert-box-container').classList.remove("in");
        }
    }, 5000);
}
function alertBoxHover(){
    document.getElementById('alert-box').classList.add('hover');
    document.getElementById('alert-box-close').innerHTML='&#10005;';
}
function alertBoxHoverOut(){
    document.getElementById('alert-box').classList.remove('hover');
    document.getElementById('alert-box-close').innerHTML='';
}
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
        url: "https://www.sosyorol.com/user-preferences/",
        async: !0,
        data: {
            uid: uid,
            sel: e,
            op: "lang"
        },
        success: function(e) {},
        error: function(e, o, t) {}
    })
}
function showHide(elemId){
    var elem = document.getElementById(elemId);
    elem.classList.toggle('hidden');
}