from django.shortcuts import render

def listarHistoricoAcesso_Ifto(request):
    context = {
        'title' : 'Histórico de Acesso',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, "pages/historico_acesso/historico_de_acesso.html", context)