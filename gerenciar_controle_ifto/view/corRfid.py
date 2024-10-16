from django.shortcuts import render
from gerenciar_controle_ifto.models import CorRFID_Funcao, Papel_pessoa

def cadastrarCorRfid(request):
    
    funcoes = Papel_pessoa.objects.filter(vinculado_corRfid=False)

    context = {
        'title' : 'Cadastro de Cor-Rfid',
        'nome_usuario_logado' : 'Rangerson',
        'funcoes' : funcoes
    }
    
    if request.method == 'POST':
        cor = request.POST.get('cor_Rfid')
        funcao = int(request.POST.get('cod_corRfid'))
        
        corRfid = CorRFID_Funcao(corRFID = cor,
                                 cod_cargo = Papel_pessoa.objects.get(pk=funcao)
                                 )
        
        corRfid.save()
        
        # Aqui ele irá atulizar o status da Funcao vinculada a cor para verdadeiro.
        edit_funcao = Papel_pessoa.objects.get(pk=funcao)
        edit_funcao.vinculado_corRfid = True
        edit_funcao.save()
        

    return render(request, "pages/corRfid/cadastrarCorRfid.html", context)

def listarCorRfid(request):

    coresRfid = CorRFID_Funcao.objects.all()
    
    context = {
        'title' : 'Listagem de Cor-Rfid',
        'coresRfid' : coresRfid,
        'nome_usuario_logado' : 'Rangerson'
    }

    return render(request, "pages/corRfid/listarCorRfid.html", context)

def editarCorRfid(request):

    context = {
        'title' : 'Editar Cor-Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }

    return render(request, "pages/corRfid/editarCorRfid.html", context)