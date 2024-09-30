from django.shortcuts import render

def home(request):
    context = {
        'title' : 'Inicío',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/homepage.html', context)