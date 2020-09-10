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