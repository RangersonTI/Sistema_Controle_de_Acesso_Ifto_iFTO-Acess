function leitura_rfid(){
    document.getElementById('tag_rfid_value').value = "";
    fetch('http://localhost:1524/ler_rfid')
        .then(response => response.json())
        .then(data => {
            document.getElementById('tag_rfid_value').value = data.rfid;
        })
        .catch(error => {
            console.error('Erro:', error);
            window.alert('Não foi possível conectar ao servidor local.');
        });
}

function leitura_rfid_listagem(){
    document.getElementById('campo').value = "";
    fetch('http://localhost:1524/ler_rfid')
        .then(response => response.json())
        .then(data => {
            document.getElementById('campo').value = data.rfid;
        })
        .catch(error => {
            console.error('Erro:', error);
            window.alert('Não foi possível conectar ao servidor local.');
        });
}

function leitura_rfid_vinculacao(){
    document.getElementById('rfid_a_vincular').value = "";
    fetch('http://localhost:1524/ler_rfid')
        .then(response => response.json())
        .then(data => {
            document.getElementById('rfid_a_vincular').value = data.rfid;
        })
        .catch(error => {
            console.error('Erro:', error);
            window.alert('Não foi possível conectar ao servidor local.');
        });
}