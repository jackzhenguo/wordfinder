var selectedTag = '';

function init(){
    $('#labelId1').hide();
    $('#clusterDiv1').hide();
}


function findByTag(selWord, rowResult, tag){
  /*
    selWord: selected word
    rowResult: sentences
    tag: POS
  */
    selectedTag = tag.textContent;
    $("#tagInput1").attr("value",selectedTag);
    var ulControl = $('#sentencesGroup');
    ulControl.find("li").remove();
    var rowResult1 = rowResult;
    if(rowResult1.length > 0){
        $('#labelId1').show();
        $('#clusterDiv1').show();
    }
    for(i=1; i<rowResult1.length+1; i++){
       var wordIndex = rowResult1[i-1].toLowerCase().indexOf(selWord.toLowerCase());
       var part1 = rowResult1[i-1].slice(0,wordIndex)
       var part2 = rowResult1[i-1].slice(wordIndex, wordIndex + selWord.length+1)
       var part3 = rowResult1[i-1].slice(wordIndex + selWord.length+1, rowResult1[i-1].length)
        var ulcontent = "<li class=\"list-group-item d-flex justify-content-between align-items-center\">"
                      + part1 + <p class="text-info"><strong>part2</strong></p> + part3 +
                      "<span class=\"badge badge-primary badge-pill\">"+i+"</span>"+"</li>";
        ulControl.append(ulcontent);
    }

}






