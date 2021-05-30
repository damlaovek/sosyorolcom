function openCloseNotifications(url){
    if(document.getElementById("notifications-c").classList.contains("dnone")){
        jQuery.ajax({
            type: "POST",
            url: url,
            success: function(response) {
                document.getElementById("notifications-c").innerHTML = response;
                document.getElementById("notifications-c").classList.remove("dnone");
                document.getElementById("num-unseen-notifications").classList.add("dnone");
            }
        });
    }else{
        document.getElementById("notifications-c").classList.add("dnone");
    }
    return false;
}
var j = jQuery.noConflict();
j(document).ready(function()
{
    j(document).mouseup(function(e) 
    {
        var container = j("#notifications-c");
        var btn = j("#notificationsbtn");

        // if the target of the click isn't the container nor a descendant of the container
        if (!container.is(e.target) && container.has(e.target).length === 0 && !btn.is(e.target) && btn.has(e.target).length === 0) 
        {
            document.getElementById("notifications-c").classList.add("dnone");
        }
    });
});
