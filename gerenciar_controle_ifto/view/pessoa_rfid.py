from django.shortcuts import render, get_object_or_404
from gerenciar_controle_ifto.formularios.PessoaForm import VincularPessoaRfid
from gerenciar_controle_ifto.models import Rfid, Pessoa
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='/iftoAcess/login/')
def vincularRfid(request, id):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

    pessoa = get_object_or_404(Pessoa, id=id)

    if request.POST:
        form = VincularPessoaRfid(request.POST)

        if form.is_valid():
            a_vincular = form.cleaned_data['rfid_a_vincular']
            cod_rfid = Rfid.objects.get(tag_rfid_value=a_vincular,vinculado=False)
            pessoa.cod_Rfid = cod_rfid
            pessoa.vinculado = True
            pessoa.save()

            rfid = get_object_or_404(Rfid,id=cod_rfid.id)
            rfid.vinculado = True
            rfid.save()
            return HttpResponseRedirect('/iftoAcess/listar/pessoa/')

        context = {
            'form' : form,
            'title' : 'Vinculação de RFID',
            'usuario_staff_atual':request.user.is_staff,
            'nome_usuario_logado' : nome_usuario
        }
        return render(request, 'pages/vincular_pessoa_rfid/vincularPessoaRfid.html', context)

    form = VincularPessoaRfid(
        initial = {
            'id' : id,
            'pessoa' : ''+pessoa.nome+' '+pessoa.sobrenome
        }
    )
    context = {
        'form' : form,
        'title' : 'Vinculação de RFID',
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/vincular_pessoa_rfid/vincularPessoaRfid.html', context)

@login_required(login_url='/iftoAcess/login/')
def desvincularRfid(request, id):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
    
    pessoa = get_object_or_404(Pessoa, id=id)

    rfid_a_desvincular = pessoa.cod_Rfid
    pessoa.cod_Rfid = None
    pessoa.vinculado = False
    pessoa.save()

    rfid = get_object_or_404(Rfid,id=rfid_a_desvincular.id)
    rfid.vinculado = False
    rfid.save()

    return HttpResponseRedirect('/iftoAcess/listar/pessoa/')