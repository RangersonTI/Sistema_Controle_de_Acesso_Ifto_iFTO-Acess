$(document).ready(function(){
    //let CampoData_desatisacao = $('#data_desativacao')
    //let CampoMotivo_desativação = $('#motivo_desativacao')
    //let CampoAtivo  = $('#rfid_ativo')
//
    //CampoData_desatisacao.prop('disable', false)
    //CampoMotivo_desativação.prop('disable', false)
//
    //if (CampoAtivo === True){
    //    CampoData_desatisacao.prop('disable', true)
    //    CampoMotivo_desativação.prop('disable', true)
    //}

    $('#rfid_ativo').click(function(){
        if($(this).is(':checked')){
            $('#data_desativacao').attr('disabled', true)
            $('#motivo_desativacao').attr('disabled', true)
        }
        else{
            $('#data_desativacao').attr('disabled', false)
            $('#motivo_desativacao').attr('disabled', false)
        }
    })

})