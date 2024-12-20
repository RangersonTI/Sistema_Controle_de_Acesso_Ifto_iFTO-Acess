
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from gerenciar_controle_ifto.formularios.LoginForm import LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime

def login_user(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            
            user_authenticate = authenticate(request, username=usuario.lower(), password=senha)
        
            if user_authenticate is not None:
                login(request,user_authenticate)
                usuario = form.cleaned_data['usuario']

                return HttpResponseRedirect('/iftoAccess/')

        context = {
            'form':form,
            'ano_criado':'2024',
            'ano_atual': str(datetime.now().year),
            'title' : 'Login',
        }
    
        return render(request, 'pages/login/login.html', context)

    form = LoginForm()

    context = {
        'form':form,
        'ano_criado':'2024',
        'ano_atual': str(datetime.now().year),
        'title' : 'Login',
    }

    return render(request, 'pages/login/login.html', context)

@login_required(login_url='/iftoAccess/login/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/iftoAccess/login/')