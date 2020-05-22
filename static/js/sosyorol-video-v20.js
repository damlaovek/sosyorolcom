var j = jQuery.noConflict();
Object.defineProperty(HTMLMediaElement.prototype, 'playing', {
    get: function(){
        return !!(this.currentTime > 0 && !this.paused && !this.ended && this.readyState > 2);
    }
});
j(window).on('load', function () {
    document.addEventListener("DOMContentLoaded", function() { startplayer(); }, false);
    player = document.getElementById('video_player');
    var seekBar = document.getElementById("seek-bar");
    
    player2 = document.getElementById('video_player2');
    var seekBar2 = document.getElementById("seek-bar2");
    if(seekBar){
    // Event listener for the seek bar
      seekBar.addEventListener("change", function() {
        // Calculate the new time
        var time = player.duration * (seekBar.value / 100);
    
        // Update the video time
        player.currentTime = time;
      });
       // Pause the video when the seek handle is being dragged
      seekBar.addEventListener("mousedown", function() {
        player.pause();
      });
      seekBar.addEventListener("mouseup", function() {
        player.play();
      });
    }
    if(seekBar2){
      seekBar2.addEventListener("change", function() {
        // Calculate the new time
        var time = player2.duration * (seekBar2.value / 100);
    
        // Update the video time
        player2.currentTime = time;
      });
      seekBar2.addEventListener("mousedown", function() {
        player2.pause();
      });
    
      // Play the video when the seek handle is dropped
      seekBar2.addEventListener("mouseup", function() {
        player2.play();
      });
    }
    if(player){
      // Update the seek bar as the video plays
      player.addEventListener("timeupdate", function() {
        // Calculate the slider value
        var value = (100 / player.duration) * player.currentTime;
    
        // Update the slider value
        seekBar.value = value;
        seekBar.style.background = 'linear-gradient(to right, #48a5e7 0%, #48a5e7 50%, #fff 50%, white 100%)';
      });
    }
    if(player2){
      player2.addEventListener("timeupdate", function() {
        // Calculate the slider value
        var value = (100 / player2.duration) * player2.currentTime;
    
        // Update the slider value
        seekBar2.value = value;
        seekBar2.style.background = 'linear-gradient(to right, #48a5e7 0%, #48a5e7 50%, #fff 50%, white 100%)';
      });
      player2.addEventListener("volumechange", function() {
          if(player2.muted){
            mute();
        }else{
            unmute();
        }
      });
    }
});
function startplayer() 
{
 player = document.getElementById('video_player');
 player.controls = false;
}
function startplayer2() 
{
 player2 = document.getElementById('video_player2');
 player2.controls = false;
}
function startStopVideo(){
    if(player.playing){
         player.pause();
        document.getElementById('video-play-large').style.display = "block";
    }else{
        play_vid();
    }
}
function startStopVideo2(){
    if(player2.playing){
         player2.pause();
        document.getElementById('video-play-large').style.display = "block";
    }else{
        play_vid2();
    }
}
function fullScreenVideo(elem){
    if(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement) {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
        player.style.maxHeight = "450px";
        exitFullscreenVideo();
    }else{
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) { /* Firefox */
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { /* IE/Edge */
            elem.msRequestFullscreen();
        }
        player.style.maxHeight = "100%";
        player.style.width = "100%";
        player.style.height = "100%";
    }
}
function fullscreen_vid(){
    var elem = document.getElementById("video-div");
    if(document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement) {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) {
            document.msExitFullscreen();
        }
        player.style.maxHeight = "450px";
        exitFullscreenVideo();
    }else{
        if (elem.requestFullscreen) {
            elem.requestFullscreen();
        } else if (elem.mozRequestFullScreen) { /* Firefox */
            elem.mozRequestFullScreen();
        } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
            elem.webkitRequestFullscreen();
        } else if (elem.msRequestFullscreen) { /* IE/Edge */
            elem.msRequestFullscreen();
        }
        player.style.maxHeight = "100%";
        player.style.width = "100%";
        player.style.height = "100%";
        fullscreenVideo();
    }
}
function play_vid()
{
document.getElementById('video-play-large').style.display = "none";
document.getElementById('pause_button').style.display="block";
document.getElementById('play_button').style.display="none";
 player.play();
}
function pause_vid()
{
 player.pause();
 document.getElementById('pause_button').style.display="none";
document.getElementById('play_button').style.display="block";
}
function stop_vid() 
{
 player.pause();
 player.currentTime = 0;
 document.getElementById('video-play-large').style.display = "block";
}
function change_vol()
{
 player.volume=document.getElementById("change_vol").value;
}
function play_vid2()
{
document.getElementById('video-play-large').style.display = "none";
 player2.play();
}
function pause_vid2()
{
 player2.pause();
}
function stop_vid2() 
{
 player2.pause();
 player2.currentTime = 0;
 document.getElementById('video-play-large').style.display = "block";
}
function mobile_vol_vid(){
    if(player2.muted){
        player2.muted = false;
        unmute();
    }else{
        player2.muted = true;
        mute();
    }
}