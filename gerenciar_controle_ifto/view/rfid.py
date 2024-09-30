from django.shortcuts import render

def cadastrarRFID(request):
    context = {
        'title' : 'Cadastro de Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/rfid/cadastrarRfid.html',context)

def editarRFID(request):
    context = {
        'title' : 'Editar Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/rfid/editarRfid.html', context)

def listarRFID(request):
    context = {
        'title' : 'Listar Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/rfid/listarRfid.html', context)