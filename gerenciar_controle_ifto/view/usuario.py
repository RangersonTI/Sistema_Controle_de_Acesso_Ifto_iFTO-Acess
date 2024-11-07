
from django.shortcuts import render
from django.contrib.auth.models import User
from gerenciar_controle_ifto.forms import UsuarioForm
from gerenciar_controle_ifto.models import Usuario_sistema

def cadastrarUsuario(request):
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        
        cod_pessoa = form.cleaned_data['cod_pessoa']
        nome = form.cleaned_data['nome']
        sobrenome = form.cleaned_data['sobrenome']
        email = form.cleaned_data['email']
        usuario = form.cleaned_data['usuario']
        senha = form.cleaned_data['senha']
        
        usuario_sys = Usuario_sistema(cod_pessoa = cod_pessoa,
                                      nome_de_usuario = nome+sobrenome,
                                      usuario = usuario,
                                      senha = senha,
                                      data_criacao = '2024-11-07' 
                                      )
        usuario_sys.save()
        
        usuario = User.objects.create_user(username=usuario,
                                            password=senha,
                                            email=email,
                                            first_name=nome,
                                            last_name=sobrenome
                                            )
        
        
        
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