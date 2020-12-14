function changeProfileImg(input, url){
    document.getElementById("profileLoader").classList.remove("dnone");
    var placeholder = document.getElementById("profileImg");
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
            placeholder.src = e.target.result;
            placeholder.style.opacity = "1";
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
                if(response.is_valid){
                    displayAlert(response.msg);
                    placeholder.src = response.url;
                    document.getElementById("profileLoader").classList.add("dnone");
                    document.getElementById('profileImgUrl').value = response.name;
                    document.getElementById('editProfileImgMenu').classList.add('hidden');
                    var j = jQuery.noConflict();
                    j("#posts").load(window.location.href + " #posts" );
                }
            }
        });
    }
}

function removeProfileImg(url){
    j.ajax({
        type: "POST",
        url: url,
        success: function(response) {
            if(response.msg){
                displayAlert(response.msg);
                document.getElementById("profileImg").src = response.url;
                document.getElementById('editProfileImgMenu').classList.add('hidden');
                var j = jQuery.noConflict();
                j("#posts").load(window.location.href + " #posts" );
            }
        }
    });
}