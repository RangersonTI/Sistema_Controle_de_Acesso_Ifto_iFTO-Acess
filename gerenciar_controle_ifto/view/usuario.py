
from django.shortcuts import render

def cadastrarUsuario(request):
    context = {
        'title' : 'Cadastro de Usuario',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/usuario/cadastrarUsuario.html', context)

def listarUsuario(request):
    context = {
        'title' : 'Editar Usuario',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/usuario/listarUsuario.html', context)


def editarUsuario(request):
    context = {
        'title' : 'Editar Usuario',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/usuario/editarUsuario.html', context)