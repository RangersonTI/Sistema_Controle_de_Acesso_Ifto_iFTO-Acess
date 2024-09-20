from django.shortcuts import render

def cadastrarRFID(request):
    context = {
        'title' : 'Cadastro de Rfid'
    }
    
    return render(request, 'rfid/cadastrarRfid.html',context)

def editarRFID(request):
    context = {
        'title' : 'Editar Rfid'
    }
    
    return render(request, 'rfid/editarRfid.html', context)

def listarRFID(request):
    context = {
        'title' : 'Listar Rfid'
    }
    
    return render(request, 'rfid/listarRfid.html', context)