// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyA9jeHII9FVkhOQfCM_NyoifnN8eIN6EFM",
    authDomain: "sosyorol-b6ab6.firebaseapp.com",
    databaseURL: "https://sosyorol-b6ab6.firebaseio.com",
    projectId: "sosyorol-b6ab6",
    storageBucket: "sosyorol-b6ab6.appspot.com",
    messagingSenderId: "565098272319",
    appId: "1:565098272319:web:5105dd611ce14cf98c8a8a",
    measurementId: "G-18ZNPD8JH4"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();
var database = firebase.database();
isEmailOrPhoneValid = false;
isUsernameValid = false;
isPasswordValid = false;
isPhone = false;
var j = jQuery.noConflict();
j("input#signup_password").on({
    keydown: function(e) {
        if (e.which === 32)
            return false;
        },
    change: function() {
        this.value = this.value.replace(/\s/g, "");
    }
});
function validateEmailOrPhone(){
    var emailOrPhone = document.getElementsByName("signup_email")[0];
    var phoneno = /(^\+?([0-9]{1,4})([0-9]{6,13}))$/;
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(emailOrPhone.value.match(phoneno)){ //it is a valid phone number
        isPhone = true;
        isEmailOrPhoneValid = true;
        document.getElementById("validemailorphone").style.display = "block";
        document.getElementById("invalidemailorphone").style.display = "none";
        document.getElementById("is_email").value = "phone"
    }else if(emailOrPhone.value.match(mailformat)){ // it is a valid email
        isPhone = false;
        isEmailOrPhoneValid = true;
        document.getElementById("validemailorphone").style.display = "block";
        document.getElementById("invalidemailorphone").style.display = "none";
        document.getElementById("is_email").value = "email"
    }else{ // invalid
        isPhone = false;
        isEmailOrPhoneValid = false;
        document.getElementById("validemailorphone").style.display = "none";
        document.getElementById("invalidemailorphone").style.display = "block";
        document.getElementById("is_email").value = ""
    }

}
function validateUsername(lengthErr, specialCharErr, alredyExistsErr, onlyNumbersErr){
    var username = document.getElementsByName("username")[0];
    var format = /[ `!@#$%^&*()+=\[\]{};':"\\|,.<>\/?~]/;
    var numbers = /^[-+_]?[0-9]+[-+_]?$/;
    if(username.value.length < 3 || username.value.length > 20){
        isUsernameValid = false;
        document.getElementById("validusername").style.display = "none";
        document.getElementById("invalidusername").style.display = "block";
        displayAlert(lengthErr);
    }else if(format.test(username.value)){
        isUsernameValid = false;
        document.getElementById("validusername").style.display = "none";
        document.getElementById("invalidusername").style.display = "block";
        displayAlert(specialCharErr);
    }else if(numbers.test(username.value)){ //contain numbers only
        isUsernameValid = false;
        document.getElementById("validusername").style.display = "none";
        document.getElementById("invalidusername").style.display = "block";
        displayAlert(onlyNumbersErr);
    }else{
        j.ajax({
            url:"checkusernamevalidity",
            type : "POST",
            data : { username: username.value},
            success : function(json) {
                if(json.is_valid){
                    isUsernameValid = true;
                    document.getElementById("validusername").style.display = "block";
                    document.getElementById("invalidusername").style.display = "none";
                }else{
                    isUsernameValid = false;
                    document.getElementById("validusername").style.display = "none";
                    document.getElementById("invalidusername").style.display = "block";
                    displayAlert(alredyExistsErr);
                }
                return true;
            }
        });
    }
}
function validatePassword(){
    var password = document.getElementsByName("signup_password")[0];
    if(password.value.length < 6){
        isPasswordValid = false;
        document.getElementById("validpassword").style.display = "none";
        document.getElementById("invalidpassword").style.display = "block";
    }else{
        isPasswordValid = true;
        document.getElementById("validpassword").style.display = "block";
        document.getElementById("invalidpassword").style.display = "none";
    }
}