
let statusL = "";
let ledBtn = document.getElementById("ledBtn")

fetch('http://192.168.1.88/data/ledStatus')
    .then(res => {
        // console.log(res.json());
        return res.json()
    })
    .then(data => {
        if(data.ledStat == 0){
            statusL = "Turn Led On"
        }
        else{
            statusL = "Turn Led Off"
        }
        // console.log(data);
        ledBtn.innerText = statusL;
    })


    
