const searchBar = document.querySelector("#search");
const searchResultsContainer = document.querySelector("#search_results_container");

searchBar.addEventListener("keyup", function(e) {
    if (e.target.value.trim().length > 0){
        getSearchResults(e.target.value);
    }else{
        searchResultsContainer.innerHTML = "";
    }
});

const getSearchResults = searchTerm => {
    searchTerm = searchTerm.toLowerCase();
    j.ajax({
        type: "POST",
        url: "/getsearchresults",
        data: {search: searchTerm},
        success: function(response) {
            showResults(searchTerm, response);
        }
    });
};

function showResults(searchTerm, results){
    searchResultsContainer.innerHTML = "";
    var index = 1;
    for (var key of Object.keys(results)) {
        var tokens = results[key].split("!:!");
        if(index == 1){
            if(tokens[0] == "community"){
                if(tokens[1] == ''){
                    tokens[1] = "http://127.0.0.1:8000/static/assets/img/defaults/default-community.png"
                    searchResultsContainer.innerHTML += "<li class='bb bt full-width ml-20 right-list-item'><a class='bsbb full-width inline-flex p020 oh' href='/c/"+key+"' target='_blank'><img src='"+tokens[1]+"' class='sqr24 p5 ml5 rounded m100 bcb img-sd'/><p class='lh34 m100 ml20 ellipsis'>Community: " + tokens[2] + "</p></a></li>";
                }else{
                    searchResultsContainer.innerHTML += "<li class='bb bt full-width ml-20 right-list-item'><a class='bsbb full-width inline-flex p020 oh' href='/c/"+key+"' target='_blank'><img src='"+tokens[1]+"' class='sqrt34 ml5 rounded m100 bcb'/><p class='lh34 m100 ml20 ellipsis'>Community: " + tokens[2] + "</p></a></li>";
                }
            }else if(tokens[0] == "post"){
                searchResultsContainer.innerHTML += "<li class='bb bt full-width ml-20 item-hover'><a class='bsbb full-width ml5' href='/"+key+"' target='_blank' style='top:-8px;'><p class='m020 lh24'>" + tokens[1]; + "</p></a></li>";
            }else if(tokens[0] == "user"){
                searchResultsContainer.innerHTML += "<li class='bb bt full-width ml-20 right-list-item'><a class='bsbb full-width inline-flex p020 oh' href='/u/"+key+"' target='_blank'><img src='"+tokens[1]+"' class='sqrt34 ml5 rounded m100'/><p class='lh34 ml20 m100 ellipsis'>Profile: " + tokens[2] + "</p></a></li>";
            }
        }else{
            if(tokens[0] == "community"){
                if(tokens[1] == ''){
                    tokens[1] = "http://127.0.0.1:8000/static/assets/img/defaults/default-community.png"
                    searchResultsContainer.innerHTML += "<li class='bb full-width ml-20 right-list-item'><a class='bsbb full-width inline-flex p020 oh' href='/c/"+key+"' target='_blank'><img src='"+tokens[1]+"' class='sqr24 p5 ml5 rounded m100 bcb img-sd'/><p class='lh34 m100 ml20 ellipsis'>Community: " + tokens[2] + "</p></a></li>";
                }else{
                    searchResultsContainer.innerHTML += "<li class='bb full-width ml-20 right-list-item'><a class='bsbb full-width inline-flex p020 oh' href='/c/"+key+"' target='_blank'><img src='"+tokens[1]+"' class='sqrt34 ml5 rounded m100 bcb'/><p class='lh34 m100 ml20 ellipsis'>Community: " + tokens[2] + "</p></a></li>";
                }
            }else if(tokens[0] == "post"){
                searchResultsContainer.innerHTML += "<li class='bb full-width ml-20 item-hover'><a class='bsbb full-width ml5' href='/"+key+"' target='_blank' style='top:-8px;'><p class='m020 lh24'>" + tokens[1]; + "</p></a></li>";
            }else if(tokens[0] == "user"){
                searchResultsContainer.innerHTML += "<li class='bb full-width ml-20 right-list-item'><a class='bsbb full-width inline-flex p020 oh' href='/u/"+key+"' target='_blank'><img src='"+tokens[1]+"' class='sqrt34 ml5 rounded m100'/><p class='lh34 ml20 m100 ellipsis'>Profile: " + tokens[2] + "</p></a></li>";
            }
        }
        index = index + 1;
    }
    if(index == 1){
        searchResultsContainer.innerHTML += "<li  class='bb bt full-width ml-20 right-list-item'><a href='/search?search_key="+searchTerm+"' class='cb inline-flex p020 oh' style='width:calc(100% - 40px);'><i class='fa fa-search p10 lh30 rounded m100 cw bcb ml5'></i><p class='m100 ml20 lh34 ellipsis'><span class='fwbold'>"+searchTerm+"</span>&nbsp;için arama yap</p></a></li>";
    }else{
        searchResultsContainer.innerHTML += "<li  class='bb full-width ml-20 right-list-item'><a href='/search?search_key="+searchTerm+"' class='cb inline-flex p020 oh' style='width:calc(100% - 40px);'><i class='fa fa-search p10 lh30 rounded m100 cw bcb ml5'></i><p class='m100 ml20 lh34 ellipsis'><span class='fwbold'>"+searchTerm+"</span>&nbsp;için arama yap</p></a></li>";
    }
}