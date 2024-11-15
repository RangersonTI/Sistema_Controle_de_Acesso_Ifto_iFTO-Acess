//function leitura_rfid(){
//    console.log('passa aqui 1.576')
//    fetch("http://localhost:8000/ler_rfid/", {method: 'GET', headers:{'Content-Type':'application/json'}}).then(response => response.json()).then(data => {
//        console.log('passa aqui 123')
//        document.getElementById('tag_rfid_value').value = data.rfid;
//        console.log(data.rfid)
//    }).catch(error => {
//        window.alert(error)
//    })
//}

document.getElementById('botao_ler_rfid').addEventListener('click', function() {
    fetch('http://localhost:8000/ler_rfid/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('tag_rfid_value').value = data.rfid;
        })
        .catch(error => {
            console.error('Erro:', error);
            window.alert('Não foi possível conectar ao servidor local.');
        });
});