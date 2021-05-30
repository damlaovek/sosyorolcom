function icerikler2(){
    document.getElementById('iceriklerim-link2').classList.add("active");
    document.getElementsByClassName('iceriklerim2')[0].style.display = "inline-block";
    document.getElementsByClassName('favorilerim2')[0].style.display = "none";
    document.getElementsByClassName('yorumlarim2')[0].style.display = "none";
    var favorilerim = document.getElementById('favorilerim-link2').classList.contains('active');
    var yorumlarim = document.getElementById('yorumlarim-link2').classList.contains('active');
    if (favorilerim){
        document.getElementById('favorilerim-link2').classList.remove('active')
    }
    if (yorumlarim){
        document.getElementById('yorumlarim-link2').classList.remove('active')
    }
    j('.category-card-left').each(function(i, obj) {
        var target = j('.category-card-right').eq(i).height();
        j('.category-card-left').eq(i).height(target);
    });
}
function favoriler2(){
    
    document.getElementById('favorilerim-link2').classList.add("active");
    document.getElementsByClassName('iceriklerim2')[0].style.display = "none";
    document.getElementsByClassName('favorilerim2')[0].style.display = "inline-block";
    document.getElementsByClassName('yorumlarim2')[0].style.display = "none";
    var iceriklerim = document.getElementById('iceriklerim-link2').classList.contains('active');
    var yorumlarim = document.getElementById('yorumlarim-link2').classList.contains('active');
    if (iceriklerim){
        document.getElementById('iceriklerim-link2').classList.remove('active')
    }
    if (yorumlarim){
        document.getElementById('yorumlarim-link2').classList.remove('active')
    }
    j('.category-card-left').each(function(i, obj) {
        var target = j('.category-card-right').eq(i).height();
        j('.category-card-left').eq(i).height(target);
    });
}
function yorumlar2(){
    document.getElementById('yorumlarim-link2').classList.add("active");
    document.getElementsByClassName('iceriklerim2')[0].style.display = "none";
    document.getElementsByClassName('favorilerim2')[0].style.display = "none";
    document.getElementsByClassName('yorumlarim2')[0].style.display = "block";
    var favorilerim = document.getElementById('favorilerim-link2').classList.contains('active');
    var iceriklerim = document.getElementById('iceriklerim-link2').classList.contains('active');
    if (favorilerim){
        document.getElementById('favorilerim-link2').classList.remove('active')
    }
    if (iceriklerim){
        document.getElementById('iceriklerim-link2').classList.remove('active')
    }
}
function takiptenCikar(){
    document.getElementById('takip-ediliyor').style.backgroundColor = "red";
    document.getElementById('takip-ediliyor').innerHTML = "Takipten Çıkar";
}
function takipEdiliyor(){
    document.getElementById('takip-ediliyor').style.backgroundColor = "rgb(72,163,230)";
    document.getElementById('takip-ediliyor').innerHTML = "Takip Ediliyor";
}

function profilEngeliKaldir(){
    document.getElementById("engelikaldir").innerHTML = "Engeli Kaldır";
    document.getElementById("engelikaldir").style.backgroundColor = "red";
}
function profilEngelle(){
    document.getElementById("engelle").innerHTML = "Engellendi";
    document.getElementById("engelle").style.backgroundColor = "rgb(72,163,230)";
    j("#mobile-profile-section").load(location.href + " #mobile-profile-section");
    j("#profile-section-2").load(location.href + " #profile-section-2");
}
function closeFollowers(){
    j("#mobile-profile-section").load(location.href + " #mobile-profile-section");
}
function openFollowers(){
    document.getElementById('mobile-profile-div').style.display = "none";
    document.getElementById('mobile-followers-popup').style.display = "block";
}
function closeFollowings(){
    j("#mobile-profile-section").load(location.href + " #mobile-profile-section");
}
function openFollowings(){
    document.getElementById('mobile-profile-div').style.display = "none";
    document.getElementById('mobile-followings-popup').style.display = "block";
}