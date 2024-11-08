
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from gerenciar_controle_ifto.forms import LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

def login_user(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            senha = form.cleaned_data['senha']
            
            user_authenticate = authenticate(request, username=usuario, password=senha)
        
            if user_authenticate is not None:
                login(request,user_authenticate)
                usuario = form.cleaned_data['usuario']

                return HttpResponseRedirect('/iftoAcess')
        
        context = {
            'form':form,
            'title' : 'Login',
        }
    
        return render(request, 'pages/login/login.html', context)
        
    form = LoginForm()
    
    context = {
            'form':form,
            'title' : 'Login',
        }
    
    return render(request, 'pages/login/login.html', context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/iftoAcess/login/')