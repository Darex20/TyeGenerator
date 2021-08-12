$("form").submit(function(){
    if ($('input:checkbox').filter(':checked').length < 1){
           alert("Please check at least one service.");
    return false;
    }
});


