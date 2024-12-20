from django.shortcuts import render
from gerenciar_controle_ifto.models import Historico_acesso_campus
from django.contrib.auth.decorators import login_required
from gerenciar_controle_ifto.models import Pessoa
from gerenciar_controle_ifto.formularios.HistoricoAcessoIfForm import *
from datetime import datetime

def converterDataHistoricoAcesso(acessos):
    for acesso in acessos:
        acesso.data_acesso = acesso.data_acesso.strftime("%d-%m-%Y %H:%M:%S")

    return acessos

@login_required(login_url='/iftoAccess/login/')
def listarHistoricoAcesso_Ifto(request):

    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

        if request.method == "POST":
            form = BuscarHistoricoAcessoForm(request.POST)

            if form.is_valid():
                campo = form.cleaned_data['campo']
                busca_data = str(form.cleaned_data['busca_data'])

                print("CAMPO: ",type(busca_data))

                if campo == None or campo=="":
                    acessos = Historico_acesso_campus.objects.all()
                    acessos = converterDataHistoricoAcesso(acessos)
                    context = {
                        'title' : 'Histórico de Acesso',
                        'form' : form,
                        'usuario_staff_atual':request.user.is_staff,
                        'acessos' : acessos,
                        'nome_usuario_logado' : nome_usuario
                    }
                    return render(request, "pages/historico_acesso/historico_de_acesso.html", context)

                if busca_data == "True":
                    acessos = Historico_acesso_campus.objects.filter(data_acesso__icontains=campo)
                    acessos = converterDataHistoricoAcesso(acessos)
                    context = {
                        'title' : 'Histórico de Acesso',
                        'form' : form,
                        'usuario_staff_atual':request.user.is_staff,
                        'acessos' : acessos,
                        'nome_usuario_logado' : nome_usuario
                    }

                    return render(request, "pages/historico_acesso/historico_de_acesso.html", context)

                pessoa=Pessoa.objects.filter(nome__icontains=campo).first()
                acessos = Historico_acesso_campus.objects.filter(cod_pessoa=pessoa)
                acessos = converterDataHistoricoAcesso(acessos)
                
                if len(acessos) <=0:
                    pessoa=Pessoa.objects.filter(sobrenome__icontains=campo).first()
                    acessos = Historico_acesso_campus.objects.filter(cod_pessoa=pessoa)
                    acessos = converterDataHistoricoAcesso(acessos)
                    
                context = {
                    'title' : 'Histórico de Acesso',
                    'form' : form,
                    'usuario_staff_atual':request.user.is_staff,
                    'acessos' : acessos,
                    'nome_usuario_logado' : nome_usuario
                }
                
                return render(request, "pages/historico_acesso/historico_de_acesso.html", context)
    
    acessos = Historico_acesso_campus.objects.all()
    
    acessos = converterDataHistoricoAcesso(acessos)
    form = BuscarHistoricoAcessoForm()
    context = {
        'title' : 'Histórico de Acesso',
        'form' : form,
        'usuario_staff_atual':request.user.is_staff,
        'acessos' : acessos,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, "pages/historico_acesso/historico_de_acesso.html", context)