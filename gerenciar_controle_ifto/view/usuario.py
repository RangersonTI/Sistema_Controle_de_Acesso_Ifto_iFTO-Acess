
from django.shortcuts import render
from gerenciar_controle_ifto.forms import UsuarioForm

def cadastrarUsuario(request):
    
    form = UsuarioForm()
    context = {
        'form':form,
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