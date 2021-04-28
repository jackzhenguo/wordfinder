var selectedTag = '';

function init(){
    $('#labelId1').hide();
    $('#clusterDiv1').hide();
}

// find all indexes of selected word(substr) in sentence(str)
function searchSubStr(str,subStr){
    var positions = new Array();
    var pos = str.indexOf(subStr);
    while(pos>-1){
        positions.push(pos);
        pos = str.indexOf(subStr,pos+1);
    }
    return positions;
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
       var allIndexes = searchSubStr(wordResultKWIC[i-1].toLowerCase(), selWord.toLowerCase());
       //var wordIndex = wordResultKWIC[i-1].toLowerCase().indexOf(selWord.toLowerCase());
       var ulcontent = "<li class=\"list-group-item d-flex justify-content-between align-items-center\"> <p>";
       if(allIndexes.length > 0){
            wordResultKWIC[i-1]
       }
       for(let i=0; i < allIndexes.length; i++){
           var part1 = wordResultKWIC[i-1].slice(0,i)
           var part2 = wordResultKWIC[i-1].slice(i, i + selWord.length)
           var part3 = wordResultKWIC[i-1].slice(i + selWord.length, wordResultKWIC[i-1].length)
           var j = i + selWord.length
           var ulcontent = ulcontent + part1 + "<strong class=\"text-success\">" + part2 + "</strong>" + part3;
        }
        ulcontent += "</p> <span class=\"badge badge-primary badge-pill\">"+i+"</span>" + "</li>";
        ulControl.append(ulcontent);
    }

}








