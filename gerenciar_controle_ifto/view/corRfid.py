from django.shortcuts import render
from gerenciar_controle_ifto.models import CorRFID_Funcao, Papel_pessoa

def cadastrarCorRfid(request):
    
    funcoes = Papel_pessoa.objects.all()

    context = {
        'title' : 'Cadastro de Cor-Rfid',
        'nome_usuario_logado' : 'Rangerson',
        'funcoes' : funcoes
    }

    return render(request, "pages/corRfid/cadastrarCorRfid.html", context)

def listarCorRfid(request):

    context = {
        'title' : 'Listagem de Cor-Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }

    return render(request, "pages/corRfid/listarCorRfid.html", context)

def editarCorRfid(request):

    context = {
        'title' : 'Editar Cor-Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }

    return render(request, "pages/corRfid/editarCorRfid.html", context)