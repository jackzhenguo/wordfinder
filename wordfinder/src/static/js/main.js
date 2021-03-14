var selectedTag = '';

function init(){
    $('#labelId1').hide();
    $('#clusterDiv1').hide();
}


function findByTag(rowResult, tag){
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
        var ulcontent = "<li class=\"list-group-item d-flex justify-content-between align-items-center\">"
                      + rowResult1[i-1] +
                      "<span class=\"badge badge-primary badge-pill\">"+i+"</span>"+"</li>";
        ulControl.append(ulcontent);
    }

}






