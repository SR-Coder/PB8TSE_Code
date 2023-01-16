// console.log("it worked!!");

let url = window.location.href;
let domain = new URL(url);


let apiStr = `http://${domain.hostname}/data/getsettingvalues`;

fetch(apiStr)
    .then(res => res.json())
    .then(res => {
        let data = JSON.parse(res);
        // console.log(data);
        for(let key in data){
            let temp = document.getElementById(key);
            if(temp == null){
                temp = document.getElementsByName(key);
                temp[data[key]].checked = true;
            } else {
                temp.value = data[key];
            }
            // console.log(temp);
        }
    })


