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
      var wordIndex = wordResultKWIC[i-1].toLowerCase().indexOf(selWord.toLowerCase());
       var part1 = wordResultKWIC[i-1].slice(0,wordIndex)
       var part2 = wordResultKWIC[i-1].slice(wordIndex, wordIndex + selWord.length+1)
       var part3 = wordResultKWIC[i-1].slice(wordIndex + selWord.length+1, wordResultKWIC[i-1].length)
       var ulcontent = "<li class=\"list-group-item d-flex justify-content-between align-items-center\">"
                      + "<p>" + part1 + "<strong class=\"text-success\">" + part2 + "</strong>" + part3 + "</p>" +
                      "<span class=\"badge badge-primary badge-pill\">"+i+"</span>"+
                      "</li>";
        ulControl.append(ulcontent);

    }

}






