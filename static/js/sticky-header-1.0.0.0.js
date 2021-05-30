var j = jQuery.noConflict();
        function arrangeHeader(){
            var scroll = j(window).scrollTop();
            var w = window.innerWidth;
            if (w >= 1142.4){
                j('.logo_sticky_header').css("display","block");
                j('.navbar').css("position","fixed");
                j('.navbar').css("top","0");
                j('.navbar').css("width","98%");
                j('.navbar').css("padding","0 1%");
                j('.navbar').css("z-index","999");
                j('#submenus-outer').css("position","fixed");
                j('#submenus-outer').css("top","50px");
                j('#submenus-outer').css("z-index","999");
                var nw = 1142.4;
                j('#submenus-outer').css("right",(w-nw)/2+"px");
                j('#searchbtn').css("background-size","16px");
                j('.navitem').each(function() {
                    this.style.fontSize = "13px";
                });
                j('#signin_link').css("font-size","13px");
                j('#downicon').css("background-size","12px");
                j('#downicon-black').css("background-size","12px");
                j('#downicon2').css("background-size","12px");
                j('.category-list-item').css("font-size","13px");
                j('#mobilheaderid').css("display","none");
            }else if( w <= 550){
                j('#mobilheaderid').css("display","block");
            }else if(w < 1142.4){
                j('.logo_sticky_header').css("display","block");
                j('.navbar').css("position","fixed");
                j('.navbar').css("top","0");
                j('.navbar').css("width","98%");
                j('.navbar').css("padding","0 1%");
                j('.navbar').css("z-index","999");
                j('#submenus-outer').css("position","fixed");
                j('#submenus-outer').css("top","50px");
                j('#submenus-outer').css("z-index","999");
                j('#submenus-outer').css("right","1%");
                j('.navitem').each(function() {
                    this.style.fontSize = "13px";
                });
                j('#searchbtn').css("background-size","16px");
                j('#signin_link').css("font-size","13px");
                j('#downicon').css("background-size","12px");
                j('#downicon-black').css("background-size","12px");
                j('#downicon2').css("background-size","12px");
                j('.category-list-item').css("font-size","13px");
                j('#mobilheaderid').css("display","none");
            }
        }
        j(document).ready(function(){ 
            arrangeHeader();
            j(window).scroll(function(){ 
                arrangeHeader();
            });
        });
        j(window).resize(function(){ 
            arrangeHeader();
        });