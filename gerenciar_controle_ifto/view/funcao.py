from django.shortcuts import render

def cadastrarFuncao(request):
    
    context = {
        'title' : 'Cadastro de Função',
        'nome_usuario_logado' : 'Rangerson'
    }
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
    return render(request, "pages/funcao/listarRfid.html", context)