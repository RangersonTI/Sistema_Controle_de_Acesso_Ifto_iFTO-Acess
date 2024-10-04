from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from gerenciar_controle_ifto.models import Papel_pessoa

def cadastrarFuncao(request):
    
    context = {
        'title' : 'Cadastro de Função',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    if request.method == 'POST':
        descricao = request.POST.get('descricao_funcao')
        
        if descricao == None:
            return HttpResponse("Campo 'Descrição' obrigatório")
        
        funcao = Papel_pessoa(descricao=descricao)
        funcao.save()
        return HttpResponseRedirect('/iftoAcess/listar/funcao/')
    
    return render(request, "pages/funcao/cadastrarFuncao.html", context)

def editarFuncao(request):
    
    context = {
        'title' : 'Editar Função',
        'nome_usuario_logado' : 'Rangerson'
    }
    return render(request, "pages/funcao/editarFuncao.html", context)

def listarFuncao(request):
    
    context = {
        'title' : 'Listagem de Função',
        'nome_usuario_logado' : 'Rangerson'
    }    
    return render(request, "pages/funcao/listarFuncao.html", context)