from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from gerenciar_controle_ifto.models import Rfid,CorRFID_Funcao
from gerenciar_controle_ifto.forms import EditarRfidForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

def converterData(rfids):
    for rfid in rfids:
        rfid.data_desativacao = rfid.data_desativacao.strftime("%d/%m/%Y, %H:%M")

    return rfids

@login_required(login_url='/iftoAcess/login/')
def cadastrarRFID(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    cores = CorRFID_Funcao.objects.all()
    
    context = {
        'title' : 'Cadastro de Tag-Rfid',
        'cores' : cores,
        'nome_usuario_logado' : nome_usuario
    }

    if request.method == 'POST':
        tag_rfid_value = request.POST.get('tag_rfid_value')
        cod_corRfid = int(request.POST.get('cod_corRfid'))
        rfid_ativo = (request.POST.get('rfid_ativo') == "on")
        motivo_desativacao = request.POST.get('motivo_desativacao')
        data_desativacao = request.POST.get('data_desativacao')

        if rfid_ativo == False:
            if request.POST.get('data_desativacao') == None:
                return HttpResponse("Campo motivo_desativação deve ser preenchido para justificar a inativação da Tag")
        else:
            data_desativacao = None

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

@login_required(login_url='/iftoAcess/login/')
def editarRFID(request, id):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username

    rfid = get_object_or_404(Rfid, id=id)

    if request.method == 'POST':
        form = EditarRfidForm(request.POST)

        if form.is_valid():
            rfid.cod_corRFID_funcao = form.cleaned_data['cod_corRFID_funcao']
            rfid.ativo = form.cleaned_data['ativo']
            rfid.data_desativacao = form.cleaned_data['data_desativacao']
            rfid.motivo_desativacao = form.cleaned_data['motivo_desativacao']
            rfid.save()
            return HttpResponseRedirect('/iftoAcess/listar/tagRfid/')
            
        context = {
            'form' : form,
            'title' : 'Edição de Tag-Rfid',
            'nome_usuario_logado' : nome_usuario
        }
        
        return render(request, 'pages/rfid/editarRfid.html', context)


    form = EditarRfidForm(
        initial={
            'tag_rfid_value': rfid.tag_rfid_value,
            'cod_corRFID_funcao': rfid.cod_corRFID_funcao,
            'ativo': rfid.ativo,
            'data_desativacao': rfid.data_desativacao,
            'motivo_desativacao': rfid.motivo_desativacao,
        },
        corRfidID = rfid.cod_corRFID_funcao.id,
    )
    
    context = {
        
        'form' : form,
        'title' : 'Edição de Tag-Rfid',
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/rfid/editarRfid.html', context)

@login_required(login_url='/iftoAcess/login/')
def listarRFID(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    rfids = Rfid.objects.all()
    #rfids = converterData(rfids)
    
    context = {
        'title' : 'Listagem de Tags-Rfid',
        'tagsRfid' : rfids,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/rfid/listarRfid.html', context)