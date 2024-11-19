function leitura_rfid(){
    fetch('http://localhost:8000/ler_rfid/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('tag_rfid_value').value = data.rfid;
        })
        .catch(error => {
            console.error('Erro:', error);
            window.alert('Não foi possível conectar ao servidor local.');
        });
}

//document.getElementById('botao_ler_rfid').addEventListener('click', function() {
//    fetch('http://localhost:8000/ler_rfid/')
//        .then(response => response.json())
//        .then(data => {
//            document.getElementById('tag_rfid_value').value = data.rfid;
//        })
//        .catch(error => {
//            console.error('Erro:', error);
//            window.alert('Não foi possível conectar ao servidor local.');
//        });
//});