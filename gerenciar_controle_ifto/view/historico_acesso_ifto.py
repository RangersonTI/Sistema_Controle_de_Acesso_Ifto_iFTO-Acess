from django.shortcuts import render
from gerenciar_controle_ifto.models import Historico_acesso_campus
from datetime import datetime

def converterDataHistoricoAcesso(acessos):
    for acesso in acessos:
        acesso.data_acesso = acesso.data_acesso.strftime("%d-%m-%Y %H:%M:%S")

    return acessos

def listarHistoricoAcesso_Ifto(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    acessos = Historico_acesso_campus.objects.all()
    
    acessos = converterDataHistoricoAcesso(acessos)
    
    context = {
        'title' : 'Histórico de Acesso',
        'acessos' : acessos,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, "pages/historico_acesso/historico_de_acesso.html", context)