$("form").submit(function(){
    if ($('input:checkbox').filter(':checked').length < 1){
           alert("Please Check at least one service");
    return false;
    }
});

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}

