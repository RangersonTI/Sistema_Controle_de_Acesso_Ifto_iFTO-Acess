from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/iftoAcess/login/')
def home(request):
    context = {
        'title' : 'Inicío',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/homepage.html', context)