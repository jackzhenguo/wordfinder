var selectedTag = '';

function init(){
    $('#labelId1').hide();
    $('#clusterDiv1').hide();
}


function findByTag(selWord, tag, rowResult, wordResultKWIC){
  /*
    selWord: selected word
    rowResult: sentences
    tag: POS

  */
    $("#tagInput1").attr("value",tag);
    var ulControl = $('#sentencesGroup');
    ulControl.find("li").remove();
    if(wordResultKWIC.length > 0){
        $('#labelId1').show();
        $('#clusterDiv1').show();
    }
    for(i=1; i<wordResultKWIC.length+1; i++){
       var ulcontent = "<li class=\"list-group-item d-flex justify-content-between align-items-center\">"
                      + "<p>" + "..." + wordResultKWIC[i-1] + "..." +"</strong></p>" +
                      "<span class=\"badge badge-primary badge-pill\">"+i+"</span>"+
                      "</li>";
        ulControl.append(ulcontent);
    }

}






