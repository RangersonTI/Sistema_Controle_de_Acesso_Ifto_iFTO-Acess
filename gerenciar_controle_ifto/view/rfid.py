from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from gerenciar_controle_ifto.models import Rfid
from datetime import datetime
def cadastrarRFID(request):
    context = {
        'title' : 'Cadastro de Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    if request.method == 'POST':
        tag_rfid_value = request.POST.get('tag_rfid_value')
        cod_corRfid = request.POST.get('cod_corRfid')
        rfid_ativo = request.POST.get('rfid_ativo')
        data_desativacao = request.POST.get('data_desativacao')
        motivo_desativacao = request.POST.get('motivo_desativacao')
        
        if tag_rfid_value == None:
            return HttpResponse("Campo Tag RFID não pode ser nulo")

        rfid = Rfid(tag_rfid_value=tag_rfid_value, 
                    cod_corRFID_funcao=cod_corRfid, 
                    data_cadastro=datetime.now().strftime('%d/%m/%y %H:%M'),
                    data_desativacao=data_desativacao,
                    ativo=rfid_ativo,
                    motivo_desativacao=motivo_desativacao
                    )
                
        rfid.save()
        return HttpResponseRedirect('/listarRFID')
        
    return render(request, 'pages/rfid/cadastrarRfid.html',context)

def editarRFID(request):
    context = {
        'title' : 'Editar Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/rfid/editarRfid.html', context)

def listarRFID(request):
    context = {
        'title' : 'Listar Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/rfid/listarRfid.html', context)