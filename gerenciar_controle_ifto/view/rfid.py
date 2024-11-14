from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from gerenciar_controle_ifto.models import Rfid,CorRFID_Funcao
from gerenciar_controle_ifto.formularios.RfidForm import *
from django.contrib.auth.decorators import login_required
from datetime import datetime

def converterData(rfids):
    for rfid in rfids:
        rfid.data_desativacao = rfid.data_desativacao.strftime("%d/%m/%Y, %H:%M")

    return rfids

@login_required(login_url='/iftoAcess/login/')
def cadastrarRFID(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

    if request.method == 'POST':
        form = CadastrarRfidForm(request.POST)

        if form.is_valid():
            rfid = Rfid(tag_rfid_value=form.cleaned_data['tag_rfid_value'],
                    cod_corRFID_funcao=form.cleaned_data['cod_corRFID_funcao'],
                    data_cadastro=datetime.now().strftime('%Y-%m-%d %H:%M'),
                    data_desativacao = form.cleaned_data['data_desativacao'],
                    vinculado = False,
                    ativo=form.cleaned_data['ativo'],
                    motivo_desativacao = form.cleaned_data['motivo_desativacao']
                    )
            
            rfid.save()
            return HttpResponseRedirect('/iftoAcess/listar/tagRfid/')
            
        context = {
            'form' : form,
            'title' : 'Edição de Tag-Rfid',
            'usuario_staff_atual':request.user.is_staff,
            'nome_usuario_logado' : nome_usuario
        }
        
        return render(request, 'pages/rfid/editarRfid.html', context)


    form = CadastrarRfidForm()
    
    context = {
        
        'form' : form,
        'title' : 'Cadastro de Tag-Rfid',
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
    }

    return render(request, 'pages/rfid/cadastrarRfid.html', context)

@login_required(login_url='/iftoAcess/login/')
def editarRFID(request, id):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

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
            'usuario_staff_atual':request.user.is_staff,
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
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/rfid/editarRfid.html', context)

@login_required(login_url='/iftoAcess/login/')
def listarRFID(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
    
    rfids = Rfid.objects.all()
    #rfids = converterData(rfids)
    
    context = {
        'title' : 'Listagem de Tags-Rfid',
        'usuario_staff_atual':request.user.is_staff,
        'tagsRfid' : rfids,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/rfid/listarRfid.html', context)