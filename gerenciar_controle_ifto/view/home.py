from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='/iftoAcess/login/')
def home(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

    
    context = {
        'title' : 'Inicío',
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/homepage.html', context)