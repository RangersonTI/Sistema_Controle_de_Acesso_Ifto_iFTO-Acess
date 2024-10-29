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
