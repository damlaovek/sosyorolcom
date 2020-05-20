function engelle(x,y,elem){
    var z = elem.innerHTML;
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/engelle/",
        data: {
            // add your parameters here
            blocker: x,
            blocking: y,
            op: z
        },
        success: function (output) {
            if(z === "Engelle"){
                elem.innerHTML ="Engeli Kaldır";
            }else{
                elem.innerHTML ="Engelle";
            }
        },
        error: function(xhr, status, error) {
        }
    });
}
function engelle2(x,y,elem){
    var z = elem.innerHTML;
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/engelle/",
        data: {
            // add your parameters here
            blocker: x,
            blocking: y,
            op: z
        },
        success: function (output) {
            if(z === "Engelle"){
                elem.innerHTML ="Engellendi";
            }else{
                elem.innerHTML ="Engelle";
            }
        },
        error: function(xhr, status, error) {
        }
    });
}
function takip(x,y,elem){
    var z = elem.innerHTML;
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/takip/",
        data: {
            // add your parameters here
            follower: x,
            following: y,
            op: z
        },
        success: function (output) {
            if(z === "Takip Et"){
                elem.innerHTML ="Takip Ediliyor";
            }else{
                elem.innerHTML ="Takip Et";
            }
        },
        error: function(xhr, status, error) {
        }
    });
}
function takip2(x,y,elem){
    var z = elem.innerHTML;
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/takip/",
        data: {
            // add your parameters here
            follower: x,
            following: y,
            op: z
        },
        success: function (output) {
            if(z === "Takip Et"){
                elem.id = 'takip-ediliyor2'; 
                elem.innerHTML ="Takip Ediliyor";
            }else{
                elem.id = 'takip-et2';
                elem.innerHTML ="Takip Et";
            }
        },
        error: function(xhr, status, error) {
        }
    });
}