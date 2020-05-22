var j = jQuery.noConflict();
j( window ).resize(function() {
    var w = window.innerWidth;
    if (w < 1142.4 && w > 550) { 
        j('.container').css("width","100%");
        j('.container-settings').css("width","100%");
        j('.container-profile').css("width","100%");
        j('.header-black-container').css("width","95%");
        j('.header-top').css("width","95%");
        j('.navbar-inner').css("width","100%");
        j('#submenus').css("width","100%");
    }else if(w <= 550){
        j('.header-top').css("width","95%");
    }else{
        j('.container').css("width","1142.4px");
        j('.container-settings').css("width","1142.4px");
        j('.container-profile').css("width","1142.4px");
        j('.header-black-container').css("width","1142.4px");
        j('.header-top').css("width","1142.4px");
        j('.navbar-inner').css("width","1142.4px");
        j('#submenus').css("width","1142.4px");
    }
});

j(document).ready(function(){ 
    var w = window.innerWidth;
    if (w < 1142.4 && w > 550) { 
        j('.container').css("width","100%");
        j('.container-settings').css("width","100%");
        j('.container-profile').css("width","100%");
        j('.header-black-container').css("width","95%");
        j('.header-top').css("width","95%");
        j('.navbar-inner').css("width","100%");
        j('#submenus').css("width","100%");
    }else if(w <= 550){
        j('.header-top').css("width","95%");
    }else{
        j('.container').css("width","1142.4px");
        j('.container-settings').css("width","1142.4px");
        j('.container-profile').css("width","1142.4px");
        j('.header-black-container').css("width","1142.4px");
        j('.header-top').css("width","1142.4px");
        j('.navbar-inner').css("width","1142.4px");
        j('#submenus').css("width","1142.4px");
    }
    j(window).scroll(function(){ 
        var w = window.innerWidth;
        if(w <= 550 && j(this).scrollTop() > 60){
            hideHesabim();
        }
        
    }); 
});
function displayMore(login) {
    document.getElementById("submenus").style.display = "block";
    var scroll = j(window).scrollTop();
    if(login && scroll > 116){
        document.getElementById("more").style.right = "194px";
        document.getElementById("more2").style.right = "194px";
        document.getElementById("more3").style.right = "194px";
        document.getElementById("more4").style.right = "194px";
        document.getElementById("more5").style.right = "194px"; 
        document.getElementById("more6").style.right = "194px";
        document.getElementById("more7").style.right = "194px"; 
        document.getElementById("more8").style.right = "194px";
        document.getElementById("more9").style.right = "194px"; 

    }else if(login){
        document.getElementById("more").style.right = "198.5px";
        document.getElementById("more2").style.right = "198.5px";
        document.getElementById("more3").style.right = "198.5px";
        document.getElementById("more4").style.right = "198.5px";
        document.getElementById("more5").style.right = "198.5px"; 
        document.getElementById("more6").style.right = "198.5px";
        document.getElementById("more7").style.right = "198.5px"; 
        document.getElementById("more8").style.right = "198.5px";
        document.getElementById("more9").style.right = "198.5px"; 
    }else if(scroll>116){
        document.getElementById("more").style.right = "198px";
        document.getElementById("more2").style.right = "186px";
        document.getElementById("more3").style.right = "198px";
        document.getElementById("more4").style.right = "198px";
        document.getElementById("more5").style.right = "198px"; 
        document.getElementById("more6").style.right = "198px";
        document.getElementById("more7").style.right = "198px"; 
        document.getElementById("more8").style.right = "198px";
        document.getElementById("more9").style.right = "198px"; 
    }else{
        document.getElementById("more").style.right = "203.5px";
        document.getElementById("more2").style.right = "203.5px";
        document.getElementById("more3").style.right = "203.5px";
        document.getElementById("more4").style.right = "203.5px";
        document.getElementById("more5").style.right = "203.5px"; 
        document.getElementById("more6").style.right = "203.5px";
        document.getElementById("more7").style.right = "203.5px"; 
        document.getElementById("more8").style.right = "203.5px";
        document.getElementById("more9").style.right = "203.5px"; 
    }
    var w = window.innerWidth;
    //alert(w);
    if (w <= 1147 && w > 1050) {
        document.getElementById("more").style.display = "none";
        document.getElementById("more2").style.display = "block";
        document.getElementById("more3").style.display = "none"; 
        document.getElementById("more4").style.display = "none"; 
        document.getElementById("more5").style.display = "none"; 
        document.getElementById("more6").style.display = "none"; 
        document.getElementById("more7").style.display = "none"; 
        document.getElementById("more8").style.display = "none"; 
        document.getElementById("more9").style.display = "none"; 
    }else if (w <= 1050 && w > 995) {
        document.getElementById("more").style.display = "none";
        document.getElementById("more2").style.display = "none";
        document.getElementById("more3").style.display = "block"; 
        document.getElementById("more4").style.display = "none"; 
        document.getElementById("more5").style.display = "none"; 
        document.getElementById("more6").style.display = "none"; 
        document.getElementById("more7").style.display = "none"; 
        document.getElementById("more8").style.display = "none"; 
        document.getElementById("more9").style.display = "none"; 
    }else if (w <= 995 && w > 891) {
        document.getElementById("more").style.display = "none";
        document.getElementById("more2").style.display = "none";
        document.getElementById("more3").style.display = "none"; 
        document.getElementById("more4").style.display = "block"; 
        document.getElementById("more5").style.display = "none"; 
        document.getElementById("more6").style.display = "none"; 
        document.getElementById("more7").style.display = "none"; 
        document.getElementById("more8").style.display = "none"; 
        document.getElementById("more9").style.display = "none"; 
    }else if (w <= 891 && w > 834) {
        document.getElementById("more").style.display = "none";
        document.getElementById("more2").style.display = "none";
        document.getElementById("more3").style.display = "none"; 
        document.getElementById("more4").style.display = "none"; 
        document.getElementById("more5").style.display = "block"; 
        document.getElementById("more6").style.display = "none"; 
        document.getElementById("more7").style.display = "none"; 
        document.getElementById("more8").style.display = "none"; 
        document.getElementById("more9").style.display = "none"; 
    }else if (w <= 834 && w > 759) {
        document.getElementById("more").style.display = "none";
        document.getElementById("more2").style.display = "none";
        document.getElementById("more3").style.display = "none"; 
        document.getElementById("more4").style.display = "none"; 
        document.getElementById("more5").style.display = "none"; 
        document.getElementById("more6").style.display = "block"; 
        document.getElementById("more7").style.display = "none"; 
        document.getElementById("more8").style.display = "none"; 
        document.getElementById("more9").style.display = "none"; 
    }else if (w <= 759 && w > 696) {
        document.getElementById("more").style.display = "none";
        document.getElementById("more2").style.display = "none";
        document.getElementById("more3").style.display = "none"; 
        document.getElementById("more4").style.display = "none"; 
        document.getElementById("more5").style.display = "none"; 
        document.getElementById("more6").style.display = "none"; 
        document.getElementById("more7").style.display = "block"; 
        document.getElementById("more8").style.display = "none"; 
        document.getElementById("more9").style.display = "none"; 
    }else if (w <= 696 && w > 603) {
        document.getElementById("more").style.display = "none";
        document.getElementById("more2").style.display = "none";
        document.getElementById("more3").style.display = "none"; 
        document.getElementById("more4").style.display = "none"; 
        document.getElementById("more5").style.display = "none"; 
        document.getElementById("more6").style.display = "none"; 
        document.getElementById("more7").style.display = "none"; 
        document.getElementById("more8").style.display = "block"; 
        document.getElementById("more9").style.display = "none"; 
    }else if (w <= 603) {
        document.getElementById("more").style.display = "none";
        document.getElementById("more2").style.display = "none";
        document.getElementById("more3").style.display = "none"; 
        document.getElementById("more4").style.display = "none"; 
        document.getElementById("more5").style.display = "none"; 
        document.getElementById("more6").style.display = "none"; 
        document.getElementById("more7").style.display = "none"; 
        document.getElementById("more8").style.display = "none"; 
        document.getElementById("more9").style.display = "block"; 
    }else{
        document.getElementById("more").style.display = "block";
        document.getElementById("more2").style.display = "none";
        document.getElementById("more3").style.display = "none"; 
        document.getElementById("more4").style.display = "none"; 
        document.getElementById("more5").style.display = "none"; 
        document.getElementById("more6").style.display = "none"; 
        document.getElementById("more7").style.display = "none"; 
        document.getElementById("more8").style.display = "none"; 
        document.getElementById("more9").style.display = "none"; 
    }
    var element = document.getElementById("morebtn");
    element.classList.add("open");
    var element2 = document.getElementById("daha-fazla");
    element2.classList.add("open");
    document.getElementById("downicon").id = "downicon-black";
}
function hideMore() {
    document.getElementById("submenus").style.display = "none";
    document.getElementById("more").style.display = "none";
    document.getElementById("more2").style.display = "none";
    document.getElementById("more3").style.display = "none"; 
    document.getElementById("more4").style.display = "none"; 
    document.getElementById("more5").style.display = "none"; 
    document.getElementById("more6").style.display = "none"; 
    document.getElementById("more7").style.display = "none"; 
    document.getElementById("more8").style.display = "none"; 
    document.getElementById("more9").style.display = "none"; 
    var element = document.getElementById("morebtn");
    element.classList.remove("open");
    var element2 = document.getElementById("daha-fazla");
    element2.classList.remove("open");
    document.getElementById("downicon-black").id = "downicon";
}
function displaySearch(){
    document.getElementById("submenus").style.display = "block";
    document.getElementById("search").style.display = "inline-flex";
    document.getElementById("ara").id = "ara-open"; 
}
function hideSearch(){
    document.getElementById("submenus").style.display = "none";
    document.getElementById("search").style.display = "none";
    document.getElementById("ara-open").id = "ara";  
}
function displaySignIn(){
    document.getElementById("submenus").style.display = "block";
    document.getElementById("signIn").style.display = "block";
    document.getElementById("signin_btn").id = "signin_btn-open"; 
    document.getElementById("signin_link").id = "signin_link-open"; 
}
function hideSignIn(){
    document.getElementById("submenus").style.display = "none";
    document.getElementById("signIn").style.display = "none";
    document.getElementById("signin_btn-open").id = "signin_btn";
    document.getElementById("signin_link-open").id = "signin_link";
}
function displayHesabim(){
    var favorilerim = document.getElementById('mobile-account-btn').classList.contains('active');
    if (favorilerim){
        hideHesabim();
    }else{
        document.getElementById('mobile-account-btn').classList.add('active');
        document.getElementById("submenus").style.display = "block";
        document.getElementById("hesabim").style.display = "block";
        document.getElementById("signin_btn").id = "signin_btn-open2"; 
        document.getElementById("signin_link").id = "signin_link-open"; 
    }
    
}
function hideHesabim(){
    var favorilerim = document.getElementById('mobile-account-btn').classList.contains('active');
    if (favorilerim){
        document.getElementById('mobile-account-btn').classList.remove('active');
    }
    document.getElementById("submenus").style.display = "none";
    document.getElementById("hesabim").style.display = "none";
    document.getElementById("signin_btn-open2").id = "signin_btn";
    document.getElementById("signin_link-open").id = "signin_link";
}
function changeTo(x, color) {
    x.style.padding = "15px 10px";
    x.style.borderTop = "2px solid "+color;
}
function changeBack(x, color) {
    x.style.padding = "16px 10px";
    x.style.borderTop = "1px solid "+color;
}