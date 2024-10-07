from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from gerenciar_controle_ifto.models import Rfid,CorRFID_Funcao
from datetime import datetime

def cadastrarRFID(request):
    
    cores = CorRFID_Funcao.objects.all()
    
    context = {
        'title' : 'Cadastro de Rfid',
        'cores' : cores,
        'nome_usuario_logado' : 'Rangerson'
    }

    print(datetime.now())
    if request.method == 'POST':
        tag_rfid_value = request.POST.get('tag_rfid_value')
        cod_corRfid = int(request.POST.get('cod_corRfid'))
        rfid_ativo = (request.POST.get('rfid_ativo') == "on")
        motivo_desativacao = request.POST.get('motivo_desativacao')
        data_desativacao = request.POST.get('data_desativacao')

        if rfid_ativo == False:
            if request.POST.get('data_desativacao') == "":
                return HttpResponse("Campo motivo_desativação deve ser preenchido para justifica a inativação da Tag")


        if tag_rfid_value == None:
            return HttpResponse("Campo Tag RFID não pode ser nulo")

        rfid = Rfid(tag_rfid_value=tag_rfid_value,
                    cod_corRFID_funcao=CorRFID_Funcao.objects.get(pk=cod_corRfid),
                    data_cadastro=datetime.now().strftime('%Y-%m-%d %H:%M'),
                    data_desativacao = data_desativacao,
                    vinculado = False,
                    ativo=rfid_ativo,
                    motivo_desativacao = motivo_desativacao
                    )
                
        rfid.save()
        return HttpResponseRedirect('/iftoAcess/listar/tagRfid/')
        
    return render(request, 'pages/rfid/cadastrarRfid.html',context)

def editarRFID(request, id_rfid):
    context = {
        'title' : 'Editar Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/rfid/editarRfid.html', context)

def listarRFID(request):
    
    rfids = Rfid.objects.all()
    
    context = {
        'title' : 'Listar Rfid',
        'tagsRfid' : rfids,
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/rfid/listarRfid.html', context)