function alltimeSosyobest(){
    document.getElementById('tum_zamanlar').style.display = "block";
    document.getElementById('gunluk').style.display = "none";
    document.getElementById('aylik').style.display = "none";
    document.getElementById('yillik').style.display = "none";
    document.getElementById('haftalik').style.display = "none";
    var hesabim = document.getElementById('daily-btn').classList.contains('active');
    if (hesabim){
        document.getElementById('daily-btn').classList.remove('active')
    }
    var hesabim2 = document.getElementById('monthly-btn').classList.contains('active');
    if (hesabim2){
        document.getElementById('monthly-btn').classList.remove('active')
    }
    var hesabim3 = document.getElementById('yearly-btn').classList.contains('active');
    if (hesabim3){
        document.getElementById('yearly-btn').classList.remove('active')
    }
    var hesabim4 = document.getElementById('weekly-btn').classList.contains('active');
    if (hesabim4){
        document.getElementById('weekly-btn').classList.remove('active')
    }
    document.getElementById('alltime-btn').classList.add("active");
}
function yearlySosyobest(){
    document.getElementById('tum_zamanlar').style.display = "none";
    document.getElementById('gunluk').style.display = "none";
    document.getElementById('aylik').style.display = "none";
    document.getElementById('yillik').style.display = "block";
    document.getElementById('haftalik').style.display = "none";
    var hesabim = document.getElementById('alltime-btn').classList.contains('active');
    if (hesabim){
        document.getElementById('alltime-btn').classList.remove('active')
    }
    var hesabim2 = document.getElementById('daily-btn').classList.contains('active');
    if (hesabim2){
        document.getElementById('daily-btn').classList.remove('active')
    }
    var hesabim3 = document.getElementById('monthly-btn').classList.contains('active');
    if (hesabim3){
        document.getElementById('monthly-btn').classList.remove('active')
    }
    var hesabim4 = document.getElementById('weekly-btn').classList.contains('active');
    if (hesabim4){
        document.getElementById('weekly-btn').classList.remove('active')
    }
    
    document.getElementById('yearly-btn').classList.add("active");
}
function monthlySosyobest(){
    document.getElementById('tum_zamanlar').style.display = "none";
    document.getElementById('gunluk').style.display = "none";
    document.getElementById('aylik').style.display = "block";
    document.getElementById('yillik').style.display = "none";
    document.getElementById('haftalik').style.display = "none";
    var hesabim = document.getElementById('alltime-btn').classList.contains('active');
    if (hesabim){
        document.getElementById('alltime-btn').classList.remove('active')
    }
    var hesabim2 = document.getElementById('daily-btn').classList.contains('active');
    if (hesabim2){
        document.getElementById('daily-btn').classList.remove('active')
    }
    var hesabim3 = document.getElementById('yearly-btn').classList.contains('active');
    if (hesabim3){
        document.getElementById('yearly-btn').classList.remove('active')
    }
    var hesabim4 = document.getElementById('weekly-btn').classList.contains('active');
    if (hesabim4){
        document.getElementById('weekly-btn').classList.remove('active')
    }
    document.getElementById('monthly-btn').classList.add("active");
}
function weeklySosyobest(){
    document.getElementById('tum_zamanlar').style.display = "none";
    document.getElementById('gunluk').style.display = "none";
    document.getElementById('aylik').style.display = "none";
    document.getElementById('yillik').style.display = "none";
    document.getElementById('haftalik').style.display = "block";
    var hesabim = document.getElementById('alltime-btn').classList.contains('active');
    if (hesabim){
        document.getElementById('alltime-btn').classList.remove('active')
    }
    var hesabim2 = document.getElementById('monthly-btn').classList.contains('active');
    if (hesabim2){
        document.getElementById('monthly-btn').classList.remove('active')
    }
    var hesabim3 = document.getElementById('yearly-btn').classList.contains('active');
    if (hesabim3){
        document.getElementById('yearly-btn').classList.remove('active')
    }
    var hesabim4 = document.getElementById('daily-btn').classList.contains('active');
    if (hesabim4){
        document.getElementById('daily-btn').classList.remove('active')
    }
    document.getElementById('weekly-btn').classList.add("active");
}
function dailySosyobest(){
    document.getElementById('tum_zamanlar').style.display = "none";
    document.getElementById('gunluk').style.display = "block";
    document.getElementById('aylik').style.display = "none";
    document.getElementById('yillik').style.display = "none";
    document.getElementById('haftalik').style.display = "none";
    var hesabim = document.getElementById('alltime-btn').classList.contains('active');
    if (hesabim){
        document.getElementById('alltime-btn').classList.remove('active')
    }
    var hesabim2 = document.getElementById('monthly-btn').classList.contains('active');
    if (hesabim2){
        document.getElementById('monthly-btn').classList.remove('active')
    }
    var hesabim3 = document.getElementById('yearly-btn').classList.contains('active');
    if (hesabim3){
        document.getElementById('yearly-btn').classList.remove('active')
    }
    var hesabim4 = document.getElementById('weekly-btn').classList.contains('active');
    if (hesabim4){
        document.getElementById('weekly-btn').classList.remove('active')
    }
    document.getElementById('daily-btn').classList.add("active");
}