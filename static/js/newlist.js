var j=jQuery.noConflict();
j(document).mouseup(function(e) {
    var container = j("#privacy-menu");
    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(e.target)) 
    {  
        if(!document.getElementById('privacy-menu').classList.contains('hidden')){
            document.getElementById('privacy-menu').classList.add('hidden');
        }
    }
});
j( document ).ready(function() {
    var title = document.getElementsByName('cp-title')[0];
    if (title.addEventListener) {
        title.addEventListener('input', function() {
        validateForm();
      }, false);
    } else if (title.attachEvent) {
        title.attachEvent('onpropertychange', function() {
        validateForm();
      });
    }
    var desc = document.getElementsByName('cp-desc')[0];
    if (desc.addEventListener) {
        desc.addEventListener('input', function() {
        validateForm();
      }, false);
    } else if (desc.attachEvent) {
        desc.attachEvent('onpropertychange', function() {
        validateForm();
      });
    }
});
function selectListPrivacy(elem, txt, privacy){
    var list = document.getElementById('privacy-menu');
    var items = list.getElementsByTagName("li");
    for (var j = 0; j < items.length; ++j) {
        items[j].classList.remove('selected');
    }
    elem.classList.add('selected');
    document.getElementById('isPrivate').value = privacy;
    document.getElementById('privacy').innerHTML = txt;
    document.getElementById('privacy-menu').classList.add('hidden');
}

function titleChanged(elem, txt){
    document.getElementById('title-placeholder').innerHTML=safe_tags_replace(elem.value);
    if(elem.value == ''){
        document.getElementById('title-placeholder').innerHTML=txt;
    }
    updateTextareaCounter(elem, 'title-counter', 25)
}
function descChanged(elem, txt, max){
    document.getElementById('desc-placeholder').innerHTML=safe_tags_replace(elem.value);
    if(elem.value == ''){
        document.getElementById('desc-placeholder').innerHTML=txt;
    }
    updateTextareaCounter(elem, 'desc-counter', max)
}

function uploadImg(input, url){
    var placeholder = document.getElementById("listImg");
    var bg = document.getElementById("listColor");
    if (input.files && input.files[0]) {
        var fd = new FormData();
        var files = input.files[0];
        var fullPath = input.value;
        if (fullPath) {
            var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
            var filename = fullPath.substring(startIndex);
            if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
                filename = filename.substring(1);
                var tokens = filename.split(".");
                if (tokens[0].length > 96) {
                    tokens[0] = tokens[0].substring(0,95);
                    filename = tokens[0].concat(tokens[1]);
                }
            }
        }
        var reader = new FileReader();
        reader.onload = function(e) {
            placeholder.style.opacity = "1";
            placeholder.src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
        fd.append('file',files,filename);
        j.ajax({
            type: "POST",
            url: url,
            data: fd,
            processData: false, 
            contentType: false,
            success: function(response) {
                alert(response.color);
                if(response.is_valid){
                    placeholder.src = response.url;
                    bg.style.backgroundColor = response.color;
                    document.getElementById('imgColor').value = response.color;
                    document.getElementById('imgUrl').value = response.name
                    validateForm();
                }
            }
        });
    }
}

String.prototype.hashCode = function(){
    var hash = 0;
    if (this.length == 0) return hash;
    for (i = 0; i < this.length; i++) {
        char = this.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash+makeid(5);
}
function makeid(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

var tagsToReplace = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;'
};

function replaceTag(tag) {
    return tagsToReplace[tag] || tag;
}

function safe_tags_replace(str) {
    return str.replace(/[&<>]/g, replaceTag);
}

function validateForm(){
    var image = document.getElementById('imageUpload');
    if(image.files.length == 0 ){
        document.getElementById('cp-sendBtn').classList.remove('active');
        document.getElementById("cp-sendBtn").disabled = true;
        return false;
    }
    var imgUrl = document.getElementById('imgUrl');
    if(imgUrl.value == ""){
        document.getElementById('cp-sendBtn').classList.remove('active');
        document.getElementById("cp-sendBtn").disabled = true;
        return false;
    }
    var title = document.getElementsByName('cp-title')[0];
    if(title.value == ""){
        document.getElementById('cp-sendBtn').classList.remove('active');
        document.getElementById("cp-sendBtn").disabled = true;
        return false;
    }
    var desc = document.getElementsByName('cp-desc')[0];
    if(desc.value == ""){
        document.getElementById('cp-sendBtn').classList.remove('active');
        document.getElementById("cp-sendBtn").disabled = true;
        return false;
    }
    document.getElementById('cp-sendBtn').classList.add('active');
    document.getElementById("cp-sendBtn").disabled = false;
    return true;
}

function saveList(csrf){
    var imgUrl = document.getElementById('imgUrl').value;
    var imgColor = document.getElementById('imgColor').value;
    var isPrivate = document.getElementById('isPrivate').value;
    var title = document.getElementsByName('cp-title')[0].value;
    var desc = document.getElementsByName('cp-desc')[0].value;
    j.ajax({
        url:"create/savenewlist/",
        type : "POST", // http method
        data : { csrfmiddlewaretoken: csrf, photo_url : imgUrl, title : title, desc: desc, color: imgColor, privacy: isPrivate}, // data sent with the post request
        // handle a successful response
        success : function(json) {
             // log the returned json to the console
            console.log("success"); // another sanity check
            return true;
        }
    });
    return false;
}