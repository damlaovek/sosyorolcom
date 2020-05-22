function favoritePost(){
    var val = j("#userid").val();
    var val2 = j("#postid").val();
    var val3 = j("#numfavs").val();
    var val4 = j("#authorid").val();
    var hesabim5 = document.getElementById('favbtn').classList.contains('active');
    if (hesabim5){
        document.getElementById('favbtn').classList.remove("active");
        val3 = parseInt(val3) - 1;
        j("#numfavs").val(val3.toString());
        document.getElementById('favcount').innerHTML = '<span>'+val3.toString()+'</span> kez favorilere eklendi';
        j.ajax({
            type: "POST",
            url: "https://www.sosyorol.com/favorilerden-cikar/",
            data: {
                // add your parameters here
                uid: val,
                pid: val2,
                aid: val4
            },
            success: function (output) {
            },
            error: function(xhr, status, error) {
            }
        });
    }else{
        document.getElementById('favbtn').classList.add("active");
        val3 = parseInt(val3) + 1;
        j("#numfavs").val(val3.toString());
        document.getElementById('favcount').innerHTML = '<span>'+val3.toString()+'</span> kez favorilere eklendi';
        j.ajax({
            type: "POST",
            url: "https://www.sosyorol.com/favorilere-ekle/",
            data: {
                // add your parameters here
                uid: val,
                pid: val2,
                aid: val4
            },
            success: function (output) {
            },
            error: function(xhr, status, error) {
            }
        });
    }
}
function favoritePost2(){
    var val = j("#userid2").val();
    var val2 = j("#postid2").val();
    var val3 = j("#numfavs2").val();
    var val4 = j("#authorid2").val();
    var hesabim5 = document.getElementById('favbtn2').classList.contains('active');
    if (hesabim5){
        document.getElementById('favbtn2').classList.remove("active");
        val3 = parseInt(val3) - 1;
        j("#numfavs2").val(val3.toString());
        document.getElementById('favcount2').innerHTML = '<span>'+val3.toString()+'</span> favori';
        j.ajax({
            type: "POST",
            url: "https://www.sosyorol.com/favorilerden-cikar/",
            data: {
                // add your parameters here
                uid: val,
                pid: val2,
                aid: val4
            },
            success: function (output) {
            },
            error: function(xhr, status, error) {
            }
        });
    }else{
        document.getElementById('favbtn2').classList.add("active");
        val3 = parseInt(val3) + 1;
        j("#numfavs2").val(val3.toString());
        document.getElementById('favcount2').innerHTML = '<span>'+val3.toString()+'</span> favori';
        j.ajax({
            type: "POST",
            url: "https://www.sosyorol.com/favorilere-ekle/",
            data: {
                // add your parameters here
                uid: val,
                pid: val2,
                aid: val4
            },
            success: function (output) {
            },
            error: function(xhr, status, error) {
            }
        });
    }
}
function ratePost(elem){
    var val = j("#userid").val();
    var val2 = j("#postid").val();
    var val3 = j("#post-points").val();
    var val4 = j("#authorid").val();
    if(elem.id === "likebtn"){
        var hesabim5 = document.getElementById('likebtn').classList.contains('active');
        if (hesabim5){
            val3 = parseInt(val3) - 1;
                    j("#post-points").val(val3.toString());
                    document.getElementById('likebtn').classList.remove('active');
                    document.getElementById('postlikecount').innerHTML = '<span>'+val3.toString()+'</span> puan';
            j.ajax({
                type: "POST",
                url: "https://www.sosyorol.com/icerige-oy-ver/",
                data: {
                    // add your parameters here
                    uid: val,
                    pid: val2,
                    opinion: '',
                    deletefirst: '',
                    aid: val4,
                    score: -1
                },
                success: function (output) {
                },
                error: function(xhr, status, error) {
                }
            });
        }else{
            var hesabim4 = document.getElementById('dislikebtn').classList.contains('active');
            if (hesabim4){
                val3 = parseInt(val3) + 2;
                        j("#post-points").val(val3.toString());
                        document.getElementById('dislikebtn').classList.remove('active');
                        document.getElementById('likebtn').classList.add('active');
                        document.getElementById('postlikecount').innerHTML = '<span>'+val3.toString()+'</span> puan';
                j.ajax({
                    type: "POST",
                    url: "https://www.sosyorol.com/icerige-oy-ver/",
                    data: {
                        // add your parameters here
                        uid: val,
                        pid: val2,
                        opinion: 'like',
                        deletefirst: 'true',
                        aid: val4,
                        score: 2
                    },
                    success: function (output) {
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }else{
                val3 = parseInt(val3) + 1;
                        j("#post-points").val(val3.toString());
                        document.getElementById('likebtn').classList.add('active');
                        document.getElementById('postlikecount').innerHTML = '<span>'+val3.toString()+'</span> puan';
                j.ajax({
                    type: "POST",
                    url: "https://www.sosyorol.com/icerige-oy-ver/",
                    data: {
                        // add your parameters here
                        uid: val,
                        pid: val2,
                        opinion: 'like',
                        deletefirst: '',
                        aid: val4,
                        score: 1
                    },
                    success: function (output) {
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }
        }
    }else{
        var hesabim3 = document.getElementById('dislikebtn').classList.contains('active');
        if (hesabim3){
            document.getElementById('dislikebtn').classList.remove("active");
                    val3 = parseInt(val3) + 1;
                    j("#post-points").val(val3.toString());
                    document.getElementById('postlikecount').innerHTML = '<span>'+val3.toString()+'</span> puan';
            j.ajax({
                type: "POST",
                url: "https://www.sosyorol.com/icerige-oy-ver/",
                data: {
                    // add your parameters here
                    uid: val,
                    pid: val2,
                    opinion: '',
                    deletefirst: '',
                    aid: val4,
                    score: 1
                },
                success: function (output) {
                    
                },
                error: function(xhr, status, error) {
                }
            });
        }else{
            var hesabim2 = document.getElementById('likebtn').classList.contains('active');
            if (hesabim2){
                document.getElementById('likebtn').classList.remove("active");
                        document.getElementById('dislikebtn').classList.add('active');
                        val3 = parseInt(val3) - 2;
                        j("#post-points").val(val3.toString());
                        document.getElementById('postlikecount').innerHTML = '<span>'+val3.toString()+'</span> puan';
                j.ajax({
                    type: "POST",
                    url: "https://www.sosyorol.com/icerige-oy-ver/",
                    data: {
                        // add your parameters here
                        uid: val,
                        pid: val2,
                        opinion: 'dislike',
                        deletefirst: 'true',
                        aid: val4,
                        score: -2
                    },
                    success: function (output) {
                        
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }else{
                document.getElementById('dislikebtn').classList.add("active");
                        val3 = parseInt(val3) - 1;
                        j("#post-points").val(val3.toString());
                        document.getElementById('postlikecount').innerHTML = '<span>'+val3.toString()+'</span> puan';
                j.ajax({
                    type: "POST",
                    url: "https://www.sosyorol.com/icerige-oy-ver/",
                    data: {
                        // add your parameters here
                        uid: val,
                        pid: val2,
                        opinion: 'dislike',
                        deletefirst: '',
                        aid: val4,
                        score: -1
                    },
                    success: function (output) {
                        
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }
        }
    }
}
function ratePost2(elem){
    var val = j("#userid2").val();
    var val2 = j("#postid2").val();
    var val3 = j("#post-points2").val();
    var val4 = j("#authorid2").val();
    if(elem.id === "likebtn2"){
        var hesabim5 = document.getElementById('likebtn2').classList.contains('active');
        if (hesabim5){
            val3 = parseInt(val3) - 1;
                    j("#post-points2").val(val3.toString());
                    document.getElementById('likebtn2').classList.remove('active');
                    document.getElementById('postlikecount2').innerHTML = '<span>'+val3.toString()+'</span> puan';
            j.ajax({
                type: "POST",
                url: "https://www.sosyorol.com/icerige-oy-ver/",
                data: {
                    // add your parameters here
                    uid: val,
                    pid: val2,
                    opinion: '',
                    deletefirst: '',
                    aid: val4,
                    score: -1
                },
                success: function (output) {
                    
                },
                error: function(xhr, status, error) {
                }
            });
        }else{
            var hesabim4 = document.getElementById('dislikebtn2').classList.contains('active');
            if (hesabim4){
                val3 = parseInt(val3) + 2;
                        j("#post-points2").val(val3.toString());
                        document.getElementById('dislikebtn2').classList.remove('active');
                        document.getElementById('likebtn2').classList.add('active');
                        document.getElementById('postlikecount2').innerHTML = '<span>'+val3.toString()+'</span> puan';
                j.ajax({
                    type: "POST",
                    url: "https://www.sosyorol.com/icerige-oy-ver/",
                    data: {
                        // add your parameters here
                        uid: val,
                        pid: val2,
                        opinion: 'like',
                        deletefirst: 'true',
                        aid: val4,
                        score: 2
                    },
                    success: function (output) {
                        
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }else{
                val3 = parseInt(val3) + 1;
                        j("#post-points").val(val3.toString());
                        document.getElementById('likebtn2').classList.add('active');
                        document.getElementById('postlikecount2').innerHTML = '<span>'+val3.toString()+'</span> puan';
                j.ajax({
                    type: "POST",
                    url: "https://www.sosyorol.com/icerige-oy-ver/",
                    data: {
                        // add your parameters here
                        uid: val,
                        pid: val2,
                        opinion: 'like',
                        deletefirst: '',
                        aid: val4,
                        score: 1
                    },
                    success: function (output) {
                        
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }
        }
    }else{
        var hesabim3 = document.getElementById('dislikebtn2').classList.contains('active');
        if (hesabim3){
            document.getElementById('dislikebtn2').classList.remove("active");
                    val3 = parseInt(val3) + 1;
                    j("#post-points2").val(val3.toString());
                    document.getElementById('postlikecount2').innerHTML = '<span>'+val3.toString()+'</span> puan';
            j.ajax({
                type: "POST",
                url: "https://www.sosyorol.com/icerige-oy-ver/",
                data: {
                    // add your parameters here
                    uid: val,
                    pid: val2,
                    opinion: '',
                    deletefirst: '',
                    aid: val4,
                    score: 1
                },
                success: function (output) {
                    
                },
                error: function(xhr, status, error) {
                }
            });
        }else{
            var hesabim2 = document.getElementById('likebtn2').classList.contains('active');
            if (hesabim2){
                document.getElementById('likebtn2').classList.remove("active");
                        document.getElementById('dislikebtn2').classList.add('active');
                        val3 = parseInt(val3) - 2;
                        j("#post-points2").val(val3.toString());
                        document.getElementById('postlikecount2').innerHTML = '<span>'+val3.toString()+'</span> puan';
                j.ajax({
                    type: "POST",
                    url: "https://www.sosyorol.com/icerige-oy-ver/",
                    data: {
                        // add your parameters here
                        uid: val,
                        pid: val2,
                        opinion: 'dislike',
                        deletefirst: 'true',
                        aid: val4,
                        score: -2
                    },
                    success: function (output) {
                        
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }else{
                document.getElementById('dislikebtn2').classList.add("active");
                        val3 = parseInt(val3) - 1;
                        j("#post-points2").val(val3.toString());
                        document.getElementById('postlikecount2').innerHTML = '<span>'+val3.toString()+'</span> puan';
                j.ajax({
                    type: "POST",
                    url: "https://www.sosyorol.com/icerige-oy-ver/",
                    data: {
                        // add your parameters here
                        uid: val,
                        pid: val2,
                        opinion: 'dislike',
                        deletefirst: '',
                        aid: val4,
                        score: -1
                    },
                    success: function (output) {
                        
                    },
                    error: function(xhr, status, error) {
                    }
                });
            }
        }
    }
}
function embedPost(index,x,y,z,t) {
    document.getElementById('post-content-id').getElementsByTagName('h4')[index].classList.add("category-card");
    var linkElement = document.getElementById('post-content-id').getElementsByTagName('h4')[index].getElementsByTagName('a')[0];
    linkElement.innerHTML = "";
    linkElement.setAttribute("id", "post-content-internal");
    var div = document.createElement('div');
    div.setAttribute("class", "category-card-right");
    var a = document.createElement('p');
    var parser = new DOMParser;
    var dom = parser.parseFromString(
        '<!doctype html><body>' + y,
        'text/html');
    var decodedString = dom.body.textContent;
    var linkText = document.createTextNode(decodedString);
    a.appendChild(linkText);
    a.setAttribute("class", "category-card-title");
    div.appendChild(a);
    var e = document.createElement('p');
    dom = parser.parseFromString(
        '<!doctype html><body>' + t,
        'text/html');
    e.innerHTML = dom.body.textContent;
    e.setAttribute("class", "embed-title");
    div.appendChild(e);
    div.classList.add("category-card-right");
    linkElement.appendChild(div);
    var rightH = div.offsetHeight;
    var thumb = document.createElement("IMG");
    thumb.setAttribute("src", z);
    thumb.setAttribute("alt", y);
    thumb.setAttribute("class", "category-card-left");
    thumb.setAttribute("height", rightH+"px");
    linkElement.appendChild(thumb);
    j('.category-card-left').each(function(i, obj) {
        var target = j('.category-card-right').eq(i).height();
        j('.category-card-left').eq(i).height(target);
    });
    document.getElementById('post-content-id').getElementsByTagName('h4')[index].style.visibility = "visible";
}
function embedPost2(index,x,y,z) {
    var linkElement = document.getElementById('post-content-id2').getElementsByTagName('h4')[index].getElementsByTagName('a')[0];
    linkElement.innerHTML = "";
    linkElement.href = x;
    var div = document.createElement('div');
    div.setAttribute("class", "category-card-right2");
    var a = document.createElement('p');
    var parser = new DOMParser;
    var dom = parser.parseFromString(
        '<!doctype html><body>' + y,
        'text/html');
    var decodedString = dom.body.textContent;
    var linkText = document.createTextNode(decodedString);
    a.appendChild(linkText);
    a.setAttribute("class", "category-card-title2");
    div.appendChild(a);
    div.classList.add("category-card-right2");
    linkElement.appendChild(div);
    var rightH = div.offsetHeight;
    var thumb = document.createElement("IMG");
    thumb.setAttribute("src", z);
    thumb.setAttribute("alt", y);
    thumb.setAttribute("class", "category-card-left2");
    thumb.setAttribute("height", rightH+"px");
    linkElement.appendChild(thumb);
    j('.category-card-left2').each(function(i, obj) {
        var target = j('.category-card-right2').eq(i).height();
        j('.category-card-left2').eq(i).height(target);
    });
}

function embedVideo() {
    var h5List = document.getElementById('post-content-id').getElementsByTagName('video');
    for (var i = 0; i < h5List.length; i++) {
        var h5 = h5List[i];
        var div = document.createElement('div');
        div.setAttribute("class", "video-bottom");
        /*
        var logo = document.createElement('p');
        logo.setAttribute("class", "video-bottom-logo");
        div.appendChild(logo);
        var texts = document.createElement('div');
        texts.setAttribute("class", "video-bottom-texts");
        var sosyorol = document.createElement('a');
        sosyorol.setAttribute("class", "video-bottom-title");
        sosyorol.href = "https://www.youtube.com/channel/UCSL4l4t_iHhSY1sboHBdFqQ";
        sosyorol.target="_blank";
        sosyorol.innerHTML = "Sosyorol";
        texts.appendChild(sosyorol);
        div.appendChild(texts);
        */
        var div2 = document.createElement('div');
        div2.setAttribute("class", "g-ytsubscribe");
        div2.setAttribute("data-channelid", "UCSL4l4t_iHhSY1sboHBdFqQ");
        div2.setAttribute("data-layout", "full");
        div2.setAttribute("data-theme", "dark");
        div2.setAttribute("data-count", "default");
        div.appendChild(div2);
        h5.appendChild(div);
    }
    var h5List = document.getElementById('post-content-id').getElementsByTagName('iframe');
    for (var i = 0; i < h5List.length; i++) {
        var h5 = h5List[i];
        var string = h5.src;
        if (string.indexOf("youtube") !== -1){
            var div = document.createElement('div');
            div.setAttribute("class", "video-bottom");
            /*
            var logo = document.createElement('p');
            logo.setAttribute("class", "video-bottom-logo");
            div.appendChild(logo);
            var texts = document.createElement('div');
            texts.setAttribute("class", "video-bottom-texts");
            var sosyorol = document.createElement('a');
            sosyorol.setAttribute("class", "video-bottom-title");
            sosyorol.href = "https://www.youtube.com/channel/UCSL4l4t_iHhSY1sboHBdFqQ";
            sosyorol.target="_blank";
            sosyorol.innerHTML = "Sosyorol";
            texts.appendChild(sosyorol);
            div.appendChild(texts);
            */
            var div2 = document.createElement('div');
            div2.setAttribute("class", "g-ytsubscribe");
            div2.setAttribute("data-channelid", "UCSL4l4t_iHhSY1sboHBdFqQ");
            div2.setAttribute("data-layout", "full");
            div2.setAttribute("data-theme", "dark");
            div2.setAttribute("data-count", "default");
            div.appendChild(div2);
            h5.appendChild(div);
        }
    }
}
function outboundsLinks(){
    var h5List = document.getElementById('post-content-id').getElementsByTagName('a');
    for (var i = 0; i < h5List.length; i++) {
        var h5 = h5List[i];
        link = h5.href;
        if(!link.includes("sosyorol.com")){
            h5.setAttribute('target', '_blank');
        }
    }
}
function outboundsLinks2(){
    var h5List = document.getElementById('post-content-id2').getElementsByTagName('a');
    for (var i = 0; i < h5List.length; i++) {
        var h5 = h5List[i];
        link = h5.href;
        if(!link.includes("sosyorol.com")){
            h5.setAttribute('target', '_blank');
        }
    }
}

function replyComment(index){
    document.getElementsByClassName("comment-text-area-form")[index].style.display = "block";
}
function cancelReply(index){
    document.getElementsByClassName("comment-text-area-form")[index].style.display = "none";
}

function begen(x,y,a,elem){
    var z = elem.innerHTML;
    var myop = z;
    t = "";
    if(z.includes("Beğenmekten Vazgeç")){
        myop = "vazgec";
        t = z.replace("Beğenmekten Vazgeç (", "");
        t = t.replace(")","");
    }else{
        myop = "begen";
        t = z.replace("Beğen (", "");
        t = t.replace(")","");
    }
    if(z === "Beğen ("+t+")"){
                var c = parseInt(t) + 1
                elem.innerHTML ="Beğenmekten Vazgeç ("+c.toString()+")";
            }else{
                var c = parseInt(t) - 1
                elem.innerHTML ="Beğen ("+c.toString()+")";
            }
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/yorumu-begen/",
        data: {
            // add your parameters here
            user: x,
            post: y,
            op: myop,
            aid: a
        },
        success: function (output) {
        },
        error: function(xhr, status, error) {
        }
    });
}
function begen2(x,y,a,elem){
    var z = elem.innerHTML;
    var myop = z;
    t = "";
    if(z.includes("Beğenmekten Vazgeç")){
        myop = "vazgec";
        t = z.replace("Beğenmekten Vazgeç (", "");
        t = t.replace(")","");
    }else{
        myop = "begen";
        t = z.replace("Beğen (", "");
        t = t.replace(")","");
    }
    if(z === "Beğen ("+t+")"){
                var c = parseInt(t) + 1
                elem.innerHTML ="Beğenmekten Vazgeç ("+c.toString()+")";
            }else{
                var c = parseInt(t) - 1
                elem.innerHTML ="Beğen ("+c.toString()+")";
            }
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/yorumu-begen/",
        data: {
            // add your parameters here
            user: x,
            post: y,
            op: myop,
            aid: a
        },
        success: function (output) {
            
        },
        error: function(xhr, status, error) {
        }
    });
}

function addComment(x,y){
    alert(x+" "+y);
    var c = document.getElementById("commenttextarea").value;
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/yorum-yaz/",
        data: {
            // add your parameters here
            user: x,
            post: y,
            pid: 0,
            ctext: c
        },
        success: function (output) {
            document.getElementById("commenttextarea").value = "";
            j("#post-comments-div").load(location.href + " #post-comments-div");
        },
        error: function(xhr, status, error) {
            alert("fail");
        }
    });
}
function yorumEkle(x,y){
    var c = document.getElementById("commenttextarea").value;
    if(c && c !== ""){
        j.ajax({
            type: "POST",
            url: "https://www.sosyorol.com/yorum-yaz/",
            data: {
                // add your parameters here
                user: x,
                post: y,
                pid: 0,
                ctext: c
            },
            success: function (output) {
                document.getElementById("commenttextarea").value = "";
                j("#post-comments-div").load(location.href + " #post-comments-div");
            },
            error: function(xhr, status, error) {
            }
        });
    }
}
function addComment2(x,y){
    var c = document.getElementById("commenttextarea2").value;
    if(c && c !== ""){
        j.ajax({
            type: "POST",
            url: "https://www.sosyorol.com/yorum-yaz/",
            data: {
                // add your parameters here
                user: x,
                post: y,
                pid: 0,
                ctext: c
            },
            success: function (output) {
                document.getElementById("commenttextarea2").value = "";
                j("#post-comments-div2").load(location.href + " #post-comments-div2");
            },
            error: function(xhr, status, error) {
            }
        });
    }
}
function addChildComment(x,y,z){
    var c = document.getElementById("childtextarea").value;
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/yorum-yaz/",
        data: {
            // add your parameters here
            user: x,
            post: y,
            pid: z,
            ctext: c
        },
        success: function (output) {
            document.getElementById("childtextarea").value = "";
            j("#post-comments-div").load(location.href + " #post-comments-div");
        },
        error: function(data) {
        }
    });
}
function addChildComment2(x,y,z){
    var c = document.getElementById("childtextarea2").value;
    j.ajax({
        type: "POST",
        url: "https://www.sosyorol.com/yorum-yaz/",
        data: {
            // add your parameters here
            user: x,
            post: y,
            pid: z,
            ctext: c
        },
        success: function (output) {
            document.getElementById("childtextarea2").value = "";
            j("#post-comments-div2").load(location.href + " #post-comments-div2");
        },
        error: function(data) {
        }
    });
}