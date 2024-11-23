from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from gerenciar_controle_ifto.models import Rfid,CorRFID_Funcao
from gerenciar_controle_ifto.formularios.RfidForm import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import datetime

def converterData(rfids):
    for rfid in rfids:
        rfid.data_cadastro = rfid.data_cadastro.strftime("%d/%m/%Y, %H:%M")
        if not(rfid.data_desativacao == None):
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
    
    rfid = get_object_or_404(Rfid, id=id)

    if rfid.vinculado:
        return HttpResponseRedirect('/iftoAcess/listar/tagRfid/')

    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

    if request.method == 'POST':
        form = EditarRfidForm(request.POST)

        if form.is_valid():
            rfid.cod_corRFID_funcao = form.cleaned_data['cod_corRFID_funcao']
            rfid.ativo = form.cleaned_data['ativo']
            if not(rfid.ativo):
                rfid.data_desativacao = form.cleaned_data['data_desativacao']
            if not(rfid.ativo):
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
        
    if request.method == "POST":
        form = BuscarRfidForm(request.POST)
        
        if form.is_valid():
            campo = form.cleaned_data['campo']
            if (campo == None or campo == ""):
                rfids = Rfid.objects.all()
                rfids = converterData(rfids)

                form = BuscarRfidForm()

                context = {
                    'title' : 'Listagem de Tags-Rfid',
                    'form' : form,
                    'usuario_staff_atual':request.user.is_staff,
                    'tagsRfid' : rfids,
                    'nome_usuario_logado' : nome_usuario
                }

                return render(request, 'pages/rfid/listarRfid.html', context)

            # Aqui fazer a filtragem pelo RFID, Função, Ativo/Não Ativo ou Disponível/Não disponível

            
            rfids = Rfid.objects.filter(tag_rfid_value__icontains=campo.upper())

            if len(rfids) <=0:
                if campo.lower() == "%at":
                    rfids = Rfid.objects.filter(ativo=True)

                if campo.lower() == "%nat":
                    rfids = Rfid.objects.filter(ativo=False)

                if campo.lower() == "%disp":
                    rfids = Rfid.objects.filter(vinculado=False,ativo=True)

                if campo.lower() == "%ndisp":
                    rfids = Rfid.objects.filter(vinculado=True,ativo=True)


            rfids = converterData(rfids)

            context = {
                'title' : 'Listagem de Tags-Rfid',
                'form' : form,
                'usuario_staff_atual':request.user.is_staff,
                'tagsRfid' : rfids,
                'nome_usuario_logado' : nome_usuario
            }

            return render(request, 'pages/rfid/listarRfid.html', context)


    rfids = Rfid.objects.all()
    rfids = converterData(rfids)

    form = BuscarRfidForm()

    context = {
        'title' : 'Listagem de Tags-Rfid',
        'form' : form,
        'usuario_staff_atual':request.user.is_staff,
        'tagsRfid' : rfids,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/rfid/listarRfid.html', context)