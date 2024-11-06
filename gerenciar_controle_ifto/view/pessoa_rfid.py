from django.shortcuts import render, get_object_or_404
from gerenciar_controle_ifto.forms import VincularPessoaRfid
from gerenciar_controle_ifto.models import Rfid, Pessoa
from django.http import HttpResponseRedirect

def vincularRfid(request, id):

    pessoa = get_object_or_404(Pessoa, id=id)

    if request.POST:
        form = VincularPessoaRfid(request.POST)

        if form.is_valid():
            print("Passou por validar")
            cod_rfid = form.cleaned_data['rfid_a_vincular']
            pessoa.cod_Rfid = cod_rfid
            pessoa.vinculado = True
            pessoa.save()

            print(f"Prinmi ai: {cod_rfid}")
            
            rfid = get_object_or_404(Rfid,id=cod_rfid.id)
            rfid.vinculado = True
            rfid.save()
            print("Vai redirecionar\n")
            return HttpResponseRedirect('/iftoAcess/listar/pessoa/')

        context = {
            'form' : form,
            'title' : 'Vinculação de RFID',
            'nome_usuario_logado' : 'Rangerson'
        }
        return render(request, 'pages/vincular_pessoa_rfid/vincularPessoaRfid.html', context)

    form = VincularPessoaRfid(
        initial = {
            'pessoa' : ''+pessoa.nome+' '+pessoa.sobrenome+' '+'('+str(pessoa.id)+')'
        },
        codCargoID = pessoa.cod_Papel_pessoa.id
    )
    context = {
        'form' : form,
        'title' : 'Vinculação de RFID',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/vincular_pessoa_rfid/vincularPessoaRfid.html', context)

def desvincularRfid(request, id):
    pessoa = get_object_or_404(Pessoa, id=id)
   
    rfid_a_desvincular = pessoa.cod_Rfid
    pessoa.cod_Rfid = None
    pessoa.vinculado = False
    pessoa.save()

    rfid = get_object_or_404(Rfid,id=rfid_a_desvincular.id)
    rfid.vinculado = False
    rfid.save()

    return HttpResponseRedirect('/iftoAcess/listar/pessoa/')
    
    #if request.method == 'POST':
    #    rfid_a_desvincular = pessoa.cod_Rfid
    #    pessoa.cod_Rfid = Null
    #    pessoa.vinculado = False
    #    pessoa.save()
    #
    #    rfid = get_object_or_404(Rfid,id=rfid_a_desvincular)
    #    rfid.vinculado = False
    #    rfid.save()
    #
    #    HttpResponseRedirect('/iftoAcess/listar/pessoa/')
#
#        context = {
#            'form' : form,
#            'title' : 'Vinculação de RFID',
 #           'nome_usuario_logado' : 'Rangerson'
 #       }
#
#    form = VincularPessoaRfid(
#        initial = {
#            'pessoa' : ''+pessoa.nome+' '+pessoa.sobrenome+' '+'('+str(pessoa.id)+')'
#        },
#        codCargoID = pessoa.cod_Papel_pessoa.id
#    )
#    context = {
#        'form' : form,
#        'title' : 'Vinculação de RFID',
#        'nome_usuario_logado' : 'Rangerson'
#    }
#    
#    return render(request, 'pages/vincular_pessoa_rfid/vincularPessoaRfid.html', context)