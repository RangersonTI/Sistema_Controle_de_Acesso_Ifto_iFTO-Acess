from django.shortcuts import render

def cadastrarPessoa(request):
    
    context = {
        'title' : 'Cadastro de Pessoa',
        'nome_usuario_logado' : 'Rangerson'
    }
    return render(request, 'pages/pessoa/cadastrarPessoa.html', context)

def listarPessoa(request):
    
    context = {
        'title' : 'Listagem de Pessoa',
        'nome_usuario_logado' : 'Rangerson'
    }
    return render(request, 'pages/pessoa/listarPessoa.html', context)