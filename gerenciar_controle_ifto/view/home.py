from django.shortcuts import render

def home(request):
    context = {
        'title' : 'Inicío'
    }
    
    return render(request, 'pages/homepage.html', context)