from django.shortcuts import render

def cadastrarRFID(request):
    return render('pessoa/cadastrarRfid.html')

def editarRFID(request):
    return render('pessoa/editarRfid.html')

def listarRFID(request):
    return render('pessoa/listarRfid.html')