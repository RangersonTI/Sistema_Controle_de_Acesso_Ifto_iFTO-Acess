$(document).ready(function(){
       
    $('#rfid_ativo').click(function(){
            if($(this).is(':checked')){
                $('#data_desativacao').attr('disabled', true)
                $('#motivo_desativacao').attr('disabled', true)
            }
            else{
                $('#data_desativacao').attr('disabled', false)
                $('#motivo_desativacao').attr('disabled', false)
            }
        }
    )
    
}
)

function desativar_campos_edRfid(){
    ativo = document.getElementById('rfid_ativo')
    console.log(ativo)
    if (ativo){
        document.getElementById('data_desativacao').attr('disabled', true)
        document.getElementById('motivo_desativacao').attr('disabled', true)
    }
}

function BuscaFormatData(){
    buscaPorData = document.getElementById('buscar_por_data');
    campo = document.getElementById('id_campo');

    if (campo){
        if (buscaPorData && buscaPorData.checked){
            campo.setAttribute('type', "date")
        }
        else{
            campo.setAttribute('type', "text")
        }

        campo.value = '';
    }
    else {
        console.error("Elemento com id 'campo' não encontrado.");
    }
}