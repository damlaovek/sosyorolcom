var googleLogin = document.getElementById("googleLogin");
googleLogin.onclick = function () {
    var o = new firebase.auth.GoogleAuthProvider();
    firebase
        .auth()
        .signInWithPopup(o)
        .then(function (o) {
            var e = o.user,
                n = e.xa,
                a = e.email;
            null != n && null != n && "" != n && (console.log(a), console.log(e.displayName)), console.log(o);
        })
        .catch(function (o) {
            console.log(o);
        });
};
var facebooklogin = document.getElementById("facebookLogin");
facebooklogin.onclick = function () {
    var o = new firebase.auth.FacebookAuthProvider();
    firebase
        .auth()
        .signInWithPopup(o)
        .then(function (o) {
            var e = o.user,
                n = e.xa,
                a = e.email;
            null != n && null != n && "" != n && (console.log(a), console.log(e.displayName)), console.log(o);
        })
        .catch(function (o) {
            console.log(o);
        });
};
var twitterlogin = document.getElementById("twitterLogin");
twitterlogin.onclick = function () {
    var o = new firebase.auth.TwitterAuthProvider();
    firebase
        .auth()
        .signInWithPopup(o)
        .then(function (o) {
            var e = o.user,
                n = e.xa,
                a = e.email;
            null != n && null != n && "" != n && (console.log(a), console.log(e.displayName)), console.log(o);
        })
        .catch(function (o) {
            console.log(o);
        });
};

function validateForm(){
    /*
        1. Check if username/email field has at least 3 characters
        2. Check if password field has at least 6 characters
    */
    var email = document.getElementsByName("email")[0].value;
    var password = document.getElementsByName("password")[0].value;
    if (email.length >= 3 && password.length >= 6){
        document.getElementsByName("login_btn")[0].disabled = false;
        return true;
    }else{
        document.getElementsByName("login_btn")[0].disabled = true;
        return false;
    }
}

function submitForm() {
    /*
        1. Check if username or email has been entered
        2. Login accordingly
    */
    var email = document.getElementsByName("email")[0].value;
    var password = document.getElementsByName("password")[0].value;
    if(email.includes("@")){ // User has entered his/her email
        console.log("User has entered his/her email");
        loginWithEmailAndPassword(email, password);
    }else{ // User has entered his/her username
        firebase.database().ref('/users/').once('value', function(snapshot) {
            snapshot.forEach(function(childSnapshot) {
                var childKey = childSnapshot.key;
                var childData = childSnapshot.val();
                if(childData.username == email){
                    console.log(childData.username);
                    var userEmail = childData.email;
                    loginWithEmailAndPassword(userEmail, password);
                }
            });
            displayAlert("User not found! Please check your credentials.");
        });
    }
    return false;
}

function loginWithEmailAndPassword(email, password){
    /*
        1. Login with email and password
        2. Set user id as session variable (uid)
    */
    var promise = firebase.auth().signInWithEmailAndPassword(email, password).catch(function(error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        displayAlert(errorMessage);
    });
    promise.then(function(){
        var user = firebase.auth().user;
        firebase.auth().onAuthStateChanged(function(user) {
            if (user) {
                console.log(user.uid);
                var signin_form = document.getElementById("signin_form");
                document.getElementsByName("uid")[0].value = user.uid;
                var j = jQuery.noConflict();
                j.ajax({
                    url:"/",
                    Type:'POST',
                    data:{uid:user.uid},
                    success:function(response){ }
                });
                signin_form.action = "/";
                signin_form.submit();
            }
        });
    });
    return false;
}
