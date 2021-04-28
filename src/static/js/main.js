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
           var startIndex = 0;
           for(let j=0; j < allIndexes.length; j++){
               var part1 = wordResultKWIC[i-1].slice(startIndex,allIndexes[j])
               var part2 = wordResultKWIC[i-1].slice(allIndexes[j], allIndexes[j] + selWord.length)
               startIndex = allIndexes[j] + selWord.length
               ulcontent = ulcontent + part1 + "<strong class=\"text-success\">" + part2 + "</strong>";
            }
            if(startIndex < wordResultKWIC[i-1].length){
               ulcontent = ulcontent + wordResultKWIC[i-1].slice(startIndex, wordResultKWIC[i-1].length)
            }
            ulcontent += "</p> <span class=\"badge badge-primary badge-pill\">"+i+"</span>" + "</li>";
            ulControl.append(ulcontent);
        }
    }

}








