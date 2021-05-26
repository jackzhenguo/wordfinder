var selectedTag = '';

function init(){
    $('#labelId1').hide();
    $('#clusterDiv1').hide();
}


function findByTag(selWord, tag, wordResultKWIC){
  /*
    selWord: selected word
    rowResult: sentences
    tag: POS
  */
    $('#clusterFunctionId1').html("<div class=\"form-group\" id=\"clusterDiv1\">" +
                "<div class=\"alert alert-dismissible alert-light my-sm-2\">" +
                    "Enter cluster count to get example sentences(examples sentences refer to representative sentences"+
                    " from results)"+
                    "<form class=\"form-inline my-2\" action=\"/cluster\" onsubmit=\"updateClusterStatus()\" method=\"post\">" +
                        "<input class=\"form-control\" type=\"text\" placeholder=\"cluster count\" id=\"clusterNumber\" name=\"clusterNumber\">"+
                        "<button class=\"btn btn-primary\" type=\"submit\" id=\"clusterId1\">Cluster</button>"+
                        "<input id=\"tagInput1\" name=\"tagInput1\" type=\"text\" hidden=\"true\">" +
                    "</form>"+
                "</div>"+
            "</div>"+
            "<div class=\"form-group\">"+
                "<label id = \"labelId1\">Sentences:</label>"+
                "<ul class=\"list-group\" id=\"sentencesGroup\" name=\"sentencesGroup\"></ul>"+
            "</div>")

    $("#tagInput1").attr("value",tag);
    var ulControl = $('#sentencesGroup');
    ulControl.find("li").remove();
    if(wordResultKWIC.length > 0){
        $('#labelId1').show();
        $('#clusterDiv1').show();
    }

    outstr = '<pre>'
    for(i=1; i<wordResultKWIC.length+1; i++){
        outstr += "<li class=\"list-group-item d-flex justify-content-between align-items-center\">" +
                        wordResultKWIC[i-1] +
                        "<span class=\"badge badge-primary badge-pill\">"+ i + "</span>" +
                  "</li>"
    }
    outstr += '</pre>'
    ulControl.append(outstr);
}

// find all indexes of selected word(substr) in sentence(str)
function searchSubStr(str,subStr){
    var positions = new Array();
    var pos = str.toLowerCase().indexOf(subStr.toLowerCase());
    while(pos>-1){
        positions.push(pos);
        pos = str.indexOf(subStr,pos+1);
    }
    return positions;
}

function updateFindStatus(){
    $('#findId1').html("<span class=\"spinner-border spinner-border-sm\"" +
                                        "role=\"status\" aria-hidden=\"true\"></span>" +
                                        "Finding...");
}


function updateClusterStatus(){
    $('#clusterId1').html("<span class=\"spinner-border spinner-border-sm\"" +
                                        "role=\"status\" aria-hidden=\"true\"></span>" +
                                        "Clustering...");
}






