function leitura_rfid(){
    fetch("http://127.0.0.1:7000/ler_rfid/").then(response => response.json()).then(data => {
        document.getElementById('tag_rfid_value').value = data.rfid;
        console.log(data.rfid)
    }).catch(error => {
        window.alert("Erro",error)
    })
}