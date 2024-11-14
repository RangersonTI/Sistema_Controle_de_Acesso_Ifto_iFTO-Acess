from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/iftoAcess/login/')
def home(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

    context = {
        'title' : 'Inicío',
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/homepage.html', context)