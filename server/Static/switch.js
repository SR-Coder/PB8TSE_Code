console.log("WE DID SOMETHING");

// This gets the domain so that we are always fetching from the correct IP address
let url = window.location.href;
let domain = new URL(url);
let apiStr = `http://${domain.hostname}/data/getconfig`;
let currdata = null

let selectElements = document.querySelectorAll('.dsel');

const setSwitch = (data) => {
    let currConf = data.currentConfig;
    let routing = data.configs[currConf].routing;
    let configs = data.configs;

    let select = document.getElementById("config");
    for(key in configs){
        let opt = document.createElement("option");
        opt.innerText = key;
        opt.value = key;
        console.log(key, currConf);
        if(key == currConf){
            opt.setAttribute('selected', true);
            opt.selected = true;
        }
        select.appendChild(opt);
    }

    console.log(configs);

    for(let i = 0; i < selectElements.length; i++){
        let idx = `s${i+1}`;
        selectElements[i].value = routing[idx];
    }

    console.log(currConf, routing, selectElements);
}


fetch(apiStr)
    .then(res => res.json())
    .then(res => {
        let data = JSON.parse(res);
        if(data != null){
            console.log("Data succesfully captured");
        }
        currdata = data;
        setSwitch(data);
    });

function showData() {
    console.log(currdata);
}

const showSaveBtn = () => {
    let container = document.querySelector(".container");
    let div = document.createElement('div');
    div.id = "save-prompt";
    let text = document.createTextNode("Click here to save: ");
    let button = document.createElement('button');
    button.innerText = "Save";
    div.appendChild(text);
    div.appendChild(button);
    container.appendChild(div);
}

const checkRouting = () =>{
    let elements = document.querySelectorAll('.dsel');
    let routes = currdata.configs[currdata.currentConfig].routing;
    let curRoutes = [];
    let selectedRoutes = [];
    for(key in routes){
        curRoutes.push(routes[key][0])
    }
    for(let i =0; i< elements.length; i++){
        selectedRoutes.push(parseInt(elements[i].value))
    }

    console.log(curRoutes, selectedRoutes);

    for(let j=0; j<curRoutes.length; j++){
        if(curRoutes[j] != selectedRoutes[j]){
            console.log("Routing has changed");
            showSaveBtn();
            return false
        }
    }
    console.log("Routing is still default");
    let saveprompt = document.getElementById("save-prompt");
    saveprompt.parentNode.removeChild(saveprompt);
    return true
}



selectElements.forEach(element => {
    element.addEventListener('change',checkRouting)
});