j(document).ready(function(){ 
    j(document).on('change', '#upload-thumb', function(){
        var property = document.getElementById("upload-thumb").files[0];
        var image_name = property.name;
        var form_data = new FormData();
        form_data.append("upload-thumb", property);
        j.ajax({
           url:"https://www.sosyorol.com/fotograf-yukle/",
           method: "POST",
           data: form_data,
           contentType:false,
           cache:false,
           processData:false,
           success:function(data)
           {
               document.getElementById("choose-photo").innerHTML = "Daha fazla fotoğraf seçin"
               document.getElementById("upload-thumbnail-container").style.display = "none";
               document.getElementById("create-post-container").style.display = "inline-flex";
               j("#uploaded-post-thumb").html(data);
               data = data.replace("<img src='", "");
               data = data.replace("' class='uploaded_img'/>", "");
               j("#thumburl").val(data);
               document.getElementById("create-post-footer").style.display = "inline-flex";
           }
        });
    });
    j(document).on('change', '#upload-image', function(){
        var property = document.getElementById("upload-image").files[0];
        var image_name = property.name;
        var form_data = new FormData();
        form_data.append("upload-thumb", property);
        j.ajax({
           url:"https://www.sosyorol.com/fotograf-yukle/",
           method: "POST",
           data: form_data,
           contentType:false,
           cache:false,
           processData:false,
           success:function(data)
           {
                j("#uploaded-post-image").html(data);
                document.getElementById("uploaded-post-image").id = "uploaded-post-image-uploaded";
                var div = document.createElement('span');
                div.setAttribute("id", "uploaded-post-image");
                document.getElementById("add-photo-to-post").appendChild(div);
                document.getElementById('upload-image').val('');
           }
        });
    });
});

function settingsHesap(){
    document.getElementById('settings-alert-box').style.display = "none";
    document.getElementById('settings-sosyalmedya-div').style.display = "none";
    document.getElementById('settings-foto-div').style.display = "none";
    document.getElementById('settings-hesap-div').style.display = "block";
    document.getElementById('settings-sifre-div').style.display = "none";
    document.getElementById('settings-engel-div').style.display = "none";
    document.getElementById('settings-uyelik-div').style.display = "none";
    var hesabim = document.getElementById('settings-sosyalmedya').classList.contains('opened');
    if (hesabim){
        document.getElementById('settings-sosyalmedya').classList.remove('opened')
    }
    var hesabim2 = document.getElementById('settings-resim').classList.contains('opened');
    if (hesabim2){
        document.getElementById('settings-resim').classList.remove('opened')
    }
    var hesabim3 = document.getElementById('settings-sifre').classList.contains('opened');
    if (hesabim3){
        document.getElementById('settings-sifre').classList.remove('opened')
    }
    var hesabim4 = document.getElementById('settings-engel').classList.contains('opened');
    if (hesabim4){
        document.getElementById('settings-engel').classList.remove('opened')
    }
    var hesabim5 = document.getElementById('settings-uyelik').classList.contains('opened');
    if (hesabim5){
        document.getElementById('settings-uyelik').classList.remove('opened')
    }
    document.getElementById('settings-hesap').classList.add("opened");
}
function settingsFoto(){
    document.getElementById('settings-alert-box').style.display = "none";
    document.getElementById('settings-sosyalmedya-div').style.display = "none";
    document.getElementById('settings-foto-div').style.display = "block";
    document.getElementById('settings-hesap-div').style.display = "none";
    document.getElementById('settings-sifre-div').style.display = "none";
    document.getElementById('settings-engel-div').style.display = "none";
    document.getElementById('settings-uyelik-div').style.display = "none";
    var hesabim2 = document.getElementById('settings-hesap').classList.contains('opened');
    if (hesabim2){
        document.getElementById('settings-hesap').classList.remove('opened');
    }
    var hesabim = document.getElementById('settings-sosyalmedya').classList.contains('opened');
    if (hesabim){
        document.getElementById('settings-sosyalmedya').classList.remove('opened');
    }
    var hesabim3 = document.getElementById('settings-sifre').classList.contains('opened');
    if (hesabim3){
        document.getElementById('settings-sifre').classList.remove('opened');
    }
    var hesabim4 = document.getElementById('settings-engel').classList.contains('opened');
    if (hesabim4){
        document.getElementById('settings-engel').classList.remove('opened');
    }
    var hesabim5 = document.getElementById('settings-uyelik').classList.contains('opened');
    if (hesabim5){
        document.getElementById('settings-uyelik').classList.remove('opened');
    }
    document.getElementById('settings-resim').classList.add("opened");
}
function settingsSosyalMedya(){
    document.getElementById('settings-alert-box').style.display = "none";
    document.getElementById('settings-sosyalmedya-div').style.display = "block";
    document.getElementById('settings-hesap-div').style.display = "none";
    document.getElementById('settings-foto-div').style.display = "none";
    document.getElementById('settings-sifre-div').style.display = "none";
    document.getElementById('settings-engel-div').style.display = "none";
    document.getElementById('settings-uyelik-div').style.display = "none";
    var hesabim = document.getElementById('settings-hesap').classList.contains('opened');
    if (hesabim){
        document.getElementById('settings-hesap').classList.remove('opened')
    }
    var hesabim2 = document.getElementById('settings-resim').classList.contains('opened');
    if (hesabim2){
        document.getElementById('settings-resim').classList.remove('opened')
    }
    var hesabim3 = document.getElementById('settings-sifre').classList.contains('opened');
    if (hesabim3){
        document.getElementById('settings-sifre').classList.remove('opened')
    }
    var hesabim4 = document.getElementById('settings-engel').classList.contains('opened');
    if (hesabim4){
        document.getElementById('settings-engel').classList.remove('opened')
    }
    var hesabim5 = document.getElementById('settings-uyelik').classList.contains('opened');
    if (hesabim5){
        document.getElementById('settings-uyelik').classList.remove('opened')
    }
    document.getElementById('settings-sosyalmedya').classList.add("opened");
}
function settingsSifre(){
    document.getElementById('settings-alert-box').style.display = "none";
    document.getElementById('settings-sosyalmedya-div').style.display = "none";
    document.getElementById('settings-hesap-div').style.display = "none";
    document.getElementById('settings-foto-div').style.display = "none";
    document.getElementById('settings-sifre-div').style.display = "block";
    document.getElementById('settings-engel-div').style.display = "none";
    document.getElementById('settings-uyelik-div').style.display = "none";
    var hesabim = document.getElementById('settings-hesap').classList.contains('opened');
    if (hesabim){
        document.getElementById('settings-hesap').classList.remove('opened')
    }
    var hesabim2 = document.getElementById('settings-resim').classList.contains('opened');
    if (hesabim2){
        document.getElementById('settings-resim').classList.remove('opened')
    }
    var hesabim3 = document.getElementById('settings-sosyalmedya').classList.contains('opened');
    if (hesabim3){
        document.getElementById('settings-sosyalmedya').classList.remove('opened')
    }
    var hesabim4 = document.getElementById('settings-engel').classList.contains('opened');
    if (hesabim4){
        document.getElementById('settings-engel').classList.remove('opened')
    }
    var hesabim5 = document.getElementById('settings-uyelik').classList.contains('opened');
    if (hesabim5){
        document.getElementById('settings-uyelik').classList.remove('opened')
    }
    document.getElementById('settings-sifre').classList.add("opened");
}
function settingsEngel(){
    document.getElementById('settings-alert-box').style.display = "none";
    document.getElementById('settings-sosyalmedya-div').style.display = "none";
    document.getElementById('settings-hesap-div').style.display = "none";
    document.getElementById('settings-foto-div').style.display = "none";
    document.getElementById('settings-sifre-div').style.display = "none";
    document.getElementById('settings-engel-div').style.display = "block";
    document.getElementById('settings-uyelik-div').style.display = "none";
    var hesabim = document.getElementById('settings-hesap').classList.contains('opened');
    if (hesabim){
        document.getElementById('settings-hesap').classList.remove('opened')
    }
    var hesabim2 = document.getElementById('settings-resim').classList.contains('opened');
    if (hesabim2){
        document.getElementById('settings-resim').classList.remove('opened')
    }
    var hesabim3 = document.getElementById('settings-sosyalmedya').classList.contains('opened');
    if (hesabim3){
        document.getElementById('settings-sosyalmedya').classList.remove('opened')
    }
    var hesabim4 = document.getElementById('settings-sifre').classList.contains('opened');
    if (hesabim4){
        document.getElementById('settings-sifre').classList.remove('opened')
    }
    var hesabim5 = document.getElementById('settings-uyelik').classList.contains('opened');
    if (hesabim5){
        document.getElementById('settings-uyelik').classList.remove('opened')
    }
    document.getElementById('settings-engel').classList.add("opened");
}
function settingsUyelik(){
    document.getElementById('settings-alert-box').style.display = "none";
    document.getElementById('settings-sosyalmedya-div').style.display = "none";
    document.getElementById('settings-hesap-div').style.display = "none";
    document.getElementById('settings-foto-div').style.display = "none";
    document.getElementById('settings-sifre-div').style.display = "none";
    document.getElementById('settings-engel-div').style.display = "none";
    document.getElementById('settings-uyelik-div').style.display = "block";
    var hesabim = document.getElementById('settings-hesap').classList.contains('opened');
    if (hesabim){
        document.getElementById('settings-hesap').classList.remove('opened')
    }
    var hesabim2 = document.getElementById('settings-resim').classList.contains('opened');
    if (hesabim2){
        document.getElementById('settings-resim').classList.remove('opened')
    }
    var hesabim3 = document.getElementById('settings-sosyalmedya').classList.contains('opened');
    if (hesabim3){
        document.getElementById('settings-sosyalmedya').classList.remove('opened')
    }
    var hesabim4 = document.getElementById('settings-sifre').classList.contains('opened');
    if (hesabim4){
        document.getElementById('settings-sifre').classList.remove('opened')
    }
    var hesabim5 = document.getElementById('settings-engel').classList.contains('opened');
    if (hesabim5){
        document.getElementById('settings-engel').classList.remove('opened')
    }
    document.getElementById('settings-uyelik').classList.add("opened");
}

function uploadThumbnail(elem){
    alert("upload");
    var file = elem.files[0];
    var formData = new FormData();
    formData.append('upload-thumb', elem);
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/fotograf-yukle/",
        type: 'POST',
        data: {
            formData: formData
        },
        contentType: false,
        processData: false,
        success: function (output) {
        },
        error: function(data) {
        }
    });
}
function closeSettingsAlert(){
    document.getElementById("settings-alert-box").style.display = "none";
}