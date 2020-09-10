var firebaseConfig = {
    apiKey: "AIzaSyA9jeHII9FVkhOQfCM_NyoifnN8eIN6EFM",
    authDomain: "sosyorol-b6ab6.firebaseapp.com",
    databaseURL: "https://sosyorol-b6ab6.firebaseio.com",
    projectId: "sosyorol-b6ab6",
    storageBucket: "sosyorol-b6ab6.appspot.com",
    messagingSenderId: "565098272319",
    appId: "1:565098272319:web:5105dd611ce14cf98c8a8a",
    measurementId: "G-18ZNPD8JH4",
};
firebase.initializeApp(firebaseConfig), firebase.analytics();
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

function submitForm() {
    //var o = document.getElementsByName("login-form")[0];
   // return o.submit(), o.reset(), !1;
    var email = document.getElementsByName("email")[0].value;
    var password = document.getElementsByName("password")[0].value;
    firebase.auth().signInWithEmailAndPassword(email, password).catch(function(error) {
        // Handle Errors here.
        var errorCode = error.code;
        var errorMessage = error.message;
        alert(errorMessage);
    });
    firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
            var signin_form = document.getElementById("signin_form");
            document.getElementsByName("uid")[0].value = user.uid;
            signin_form.action = "/";
            signin_form.submit();
        }
    });
    return false;
}
