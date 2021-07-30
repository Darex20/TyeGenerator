$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
    });

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

/* function generateTyeFile(){
    // TODO, hardcoded input
var output =`name: myapplication
services:
- name: backend
project: backend/backend.csproj
bindings:
- port: 7000
- name: frontend
project: frontend/frontend.csproj
replicas: 2
bindings:
- port: 8000
- name: worker
project: worker/worker.csproj
- name: rabbit
image: rabbitmq:3-management
bindings:
- port: 5672
protocol: rabbitmq`;

    download("tye.yaml", output);    
}
*/
