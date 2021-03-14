function postFindData(){
    var language_name = $('#sellanguage1').text();
    var sel_word_val = $('#selword1').val();
    $.ajax({
            type: "POST",
            url: "/find2",
            contentType: "application/json",
            data: JSON.stringify({"language_name": language_name,
                                  "sel_word": sel_word_val}),
            dataType: "json",
            success: function (response) {
                console.log(response);
            },
            error: function (err) {
                console.log(err);
            }
        });
    }
