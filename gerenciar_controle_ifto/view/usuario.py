
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from gerenciar_controle_ifto.forms import UsuarioForm
from gerenciar_controle_ifto.models import Usuario_sistema
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def cadastrarUsuario(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username

    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
        #cod_pessoa = form.cleaned_data['cod_pessoa']
            nome = form.cleaned_data['nome']
            sobrenome = form.cleaned_data['sobrenome']
            email = form.cleaned_data['email']
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            ativo = form.cleaned_data['ativo']

        #usuario_sys = Usuario_sistema(cod_pessoa = cod_pessoa,
        #                              nome_de_usuario = nome+sobrenome,
        #                              usuario = usuario,
        #                              senha = senha,
        #                              data_criacao = '2024-11-07' 
        #                              )
        #usuario_sys.save()

            usuario = User.objects.create_user(username=usuario.lower(),
                                               password=senha,
                                               email=email,
                                               first_name=nome,
                                               last_name=sobrenome,
                                               is_active=ativo
                                                )
            usuario.save()
            return HttpResponseRedirect('/iftoAcess/listar/usuario/')
        
        context = {
            'form':form,
            'title' : 'Cadastro de Usuario',
            'nome_usuario_logado' : nome_usuario
        }
    
        return render(request, 'pages/usuario/cadastrarUsuario.html', context)
        
    form = UsuarioForm()
    context = {
        'form':form,
        'title' : 'Cadastro de Usuario',
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/usuario/cadastrarUsuario.html', context)

def listarUsuario(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    usuarios = User.objects.all()
    
    context = {
        'usuarios':usuarios,
        'title' : 'Editar Usuario',
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/usuario/listarUsuario.html', context)


def editarUsuario(request, id):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    usuario = get_object_or_404(User,id=id)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
        #cod_pessoa = form.cleaned_data['cod_pessoa']
            usuario.first_name= (form.cleaned_data['nome']).lower()
            print(usuario.first_name)
            usuario.last_name = form.cleaned_data['sobrenome']
            usuario.email = form.cleaned_data['email']
            usuario.username = form.cleaned_data['usuario']
            usuario.set_password(form.cleaned_data['senha'])
            usuario.is_active = form.cleaned_data['ativo']
            usuario.save()

        #usuario_sys = Usuario_sistema(cod_pessoa = cod_pessoa,
        #                              nome_de_usuario = nome+sobrenome,
        #                              usuario = usuario,
        #                              senha = senha,
        #                              data_criacao = '2024-11-07' 
        #                              )
        #usuario_sys.save()
        
            return HttpResponseRedirect('/iftoAcess/listar/usuario/')
        
        context = {
            'form':form,
            'title' : 'Edicao de Usuario',
            'nome_usuario_logado' : nome_usuario
        }

        return render(request, 'pages/usuario/cadastrarUsuario.html', context)

    form = UsuarioForm(
        initial = {
            'usuario':usuario.username.lower(),
            'senha':usuario.password,
            'email':usuario.email,
            'nome':usuario.first_name,
            'sobrenome':usuario.last_name,
            'ativo':usuario.is_active
        },
        #cod_user_id = usuario.id
    )
    
    context = {
        'form':form,
        'title' : 'Edicao de Usuario',
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/usuario/cadastrarUsuario.html', context)