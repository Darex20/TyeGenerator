function showInput(id){
    if (document.getElementById(id).style.display == "none"){
        document.getElementById(id).style.display = "inline";
    } else {
        document.getElementById(id).style.display = "none";
        document.getElementById(id).value = "";
    }
}

function checkDuplicate(services){
    var name = document.getElementById("service_name").value;
    var services = document.getElementById("services").textContent.trim().replaceAll("\'", "\"");
    console.log(name)
    console.log(services)
    if (services.includes(name)){
        alert("Service name " + name + " is already in database. Please use another name.")
        return false;
    } else {
        document.getElementById("form").submit();
        return true;
    }
}

