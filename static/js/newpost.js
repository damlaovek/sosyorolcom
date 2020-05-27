var j = jQuery.noConflict();
            j(document).mouseup(function(e) {
                var container = j("#poll-duration-menu");
                // if the target of the click isn't the container nor a descendant of the container
                if (!container.is(e.target)) 
                {  
                    if(!document.getElementById('poll-duration-menu').classList.contains('hidden')){
                        document.getElementById('poll-duration-menu').classList.add('hidden');
                    }
                }
            });
            j( document ).ready(function() {
                var parentElement = document.getElementById('cp-container');
                var area = document.body.querySelector('textarea');
                if (area.addEventListener) {
                  area.addEventListener('input', function() {
                    validateForm();
                  }, false);
                } else if (area.attachEvent) {
                  area.attachEvent('onpropertychange', function() {
                    validateForm();
                  });
                }
                var optionList = document.getElementById('poll-options-list').children;
                var i;
                for(i = 0; i < optionList.length; i++){
                    area = optionList[i].getElementsByTagName('div')[0].getElementsByTagName('textarea')[0];
                    if (area.addEventListener) {
                      area.addEventListener('input', function() {
                        validateForm();
                      }, false);
                    } else if (area.attachEvent) {
                      area.attachEvent('onpropertychange', function() {
                        validateForm();
                      });
                    }
                }
            });
            function addSelectedCommunity(elem){
                var liId = document.getElementById("selected-communities").length + 1;
                var imgUrl = elem.getElementsByTagName('img')[0].src;
                var bc = elem.getElementsByTagName('img')[0].style.backgroundColor;
                var commName = elem.getElementsByTagName('p')[0].innerHTML;
                var li = document.createElement('li');
                li.setAttribute("class","inline-flex btn left p010 selected-community");
                li.setAttribute("id","selected-community-"+liId);
                li.style.height = "30px";
                li.style.borderRadius = "15px";
                li.style.opacity = "1";
                var img = document.createElement('img');
                img.style.backgroundColor = bc;
                img.src = imgUrl;
                img.setAttribute("class","rounded sqr20");
                img.style.margin = "5px 0";
                var p = document.createElement('p');
                p.innerHTML = commName;
                p.setAttribute("class","lh20 fs14");
                p.style.margin = "5px 10px";
                var x = document.createElement('p');
                x.setAttribute("class","fs14 lh20 hand");
                x.style.margin = "6px 0";
                x.innerHTML = "&#x2715";
                x.setAttribute("onclick","document.getElementById('selected-community-"+liId+"').remove()");
                li.appendChild(img);
                li.appendChild(p);
                li.appendChild(x);
                document.getElementById("selected-communities").appendChild(li);
            }
            function selectPollDuration(elem, txt){
                var list = document.getElementById('poll-duration-menu');
                var items = list.getElementsByTagName("li");
                for (var j = 0; j < items.length; ++j) {
                    items[j].classList.remove('selected');
                }
                elem.classList.add('selected');
                document.getElementById('poll-duration').innerHTML = txt;
                document.getElementById('poll-duration-menu').classList.add('hidden');
            }
            function validateForm(){
                var title = document.getElementsByName('cp-title')[0];
                if(title.value == ""){
                    document.getElementById('cp-sendBtn').classList.remove('active');
                    document.getElementById("cp-sendBtn").disabled = true;
                    return false;
                }
                var body = document.getElementsByName('richTextField')[0];
                if(body.contentDocument.body.innerHTML == ""){
                    document.getElementById('cp-sendBtn').classList.remove('active');
                    document.getElementById("cp-sendBtn").disabled = true;
                    return false;
                }
                var optionList = document.getElementById('poll-options-list').children;
                var div1 = optionList[0].getElementsByTagName('div')[0];
                var textarea1 = div1.getElementsByTagName('textarea')[0];
                var div2 = optionList[1].getElementsByTagName('div')[0];
                var textarea2 = div2.getElementsByTagName('textarea')[0];
                if(textarea1.value == "" || textarea2.value == ""){
                    document.getElementById('cp-sendBtn').classList.remove('active');
                    document.getElementById("cp-sendBtn").disabled = true;
                    return false;
                }
                var duration = document.getElementsByClassName('poll-duration-menu-item selected');
                if(duration.length == 0){
                    document.getElementById('cp-sendBtn').classList.remove('active');
                    document.getElementById("cp-sendBtn").disabled = true;
                    return false;
                }
                document.getElementById('cp-sendBtn').classList.add('active');
                document.getElementById("cp-sendBtn").disabled = false;
                return true;
            }