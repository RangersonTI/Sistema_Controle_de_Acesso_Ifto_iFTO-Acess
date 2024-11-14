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

// Setar data maxima do campo de data_nascimento em cadastro/editar pessoa

//var hoje = new Date();
//var dia = hoje.getDate();
//var mes = hoje.getMonth() + 1;
//var ano = hoje.getFullYear();
//
//hoje = ano+'-'+mes+'-'+dia+'';
//
//if (dia < 10){
//    dia = '0'+dia;
//}
//
//if (mes < 10){
//    mes = '0'+mes;
//}
//
//document.getElementById("data_nascimento").setAttribute("max", hoje)
