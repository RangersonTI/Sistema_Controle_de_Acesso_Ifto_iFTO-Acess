from django.shortcuts import render
from gerenciar_controle_ifto.models import Historico_acesso_campus
from django.contrib.auth.decorators import login_required
from gerenciar_controle_ifto.models import Pessoa, Rfid, Papel_pessoa
from gerenciar_controle_ifto.formularios.HistoricoAcessoIfForm import *
from datetime import datetime

def converterDataHistoricoAcesso(acessos):
    for acesso in acessos:
        acesso.data_acesso = acesso.data_acesso.strftime("%d-%m-%Y %H:%M:%S")

    return acessos

@login_required(login_url='/iftoAcess/login/')
def listarHistoricoAcesso_Ifto(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
        
        if request.method == "POST":
            form = BuscarRfidForm(request.POST)
            
            if form.is_valid():
                campo = form.cleaned_data['campo']
                
                if campo == None or campo=="":
                    
                    acessos = Historico_acesso_campus.objects.all()
                    acessos = converterDataHistoricoAcesso(acessos)
                    form = BuscarRfidForm()
                    context = {
                        'title' : 'Histórico de Acesso',
                        'usuario_staff_atual':request.user.is_staff,
                        'acessos' : acessos,
                        'nome_usuario_logado' : nome_usuario
                    }
                    
                    return render(request, "pages/historico_acesso/historico_de_acesso.html", context)
                
                #pessoas = Pessoa.objects.filter(nome=campo)
                acessos = Historico_acesso_campus.objects.filter(data_acesso="")
                
                #if len(pessoas) <=0:
                #    pessoas = Pessoa.objects.filter(sobrenome=campo)
                #    
                #if len(pessoas) <=0:
                #    pessoas = Pessoa.objects.filter(sobrenome=campo)
                #    acessos = Historico_acesso_campus.objects.filter()
                #acessos = converterDataHistoricoAcesso(acessos)
    
    acessos = Historico_acesso_campus.objects.all()
    
    acessos = converterDataHistoricoAcesso(acessos)
    form = BuscarRfidForm()
    context = {
        'title' : 'Histórico de Acesso',
        'form' : form,
        'usuario_staff_atual':request.user.is_staff,
        'acessos' : acessos,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, "pages/historico_acesso/historico_de_acesso.html", context)