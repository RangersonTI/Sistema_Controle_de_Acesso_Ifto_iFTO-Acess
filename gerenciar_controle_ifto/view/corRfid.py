from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from gerenciar_controle_ifto.models import CorRFID_Funcao, Papel_pessoa
from gerenciar_controle_ifto.forms import EditarCorRfidForm

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


def editarCorRfid(request, id):
    
    cor_rfid_funcao = get_object_or_404(CorRFID_Funcao, id=id)
    
    if request.method == 'POST':
        form = EditarCorRfidForm(request.POST)
        
        if form.is_valid:
            cor_rfid_funcao.corRFID = form.cleaned_data['cor_Rfid']
            cor_rfid_funcao.cod_cargo = form.cleaned_data['cod_corRfid']
            cor_rfid_funcao.save()
            
            return HttpResponseRedirect('/iftoAcess/listar/corRfid/')
        
        context = {
            'form' : form,
            'title' : 'Edicao de Cor-Rfid',
            'nome_usuario_logado' : 'Rangerson'
        }
        return render(request, 'pages/corRfid/editarCorRfid.html', context)
        
        
    context = {
        'form' : form,
        'title' : 'Edicao de Cor-Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    return render(request, 'pages/corRfid/editarCorRfid.html', context)
    
    form = EditarCorRfidForm(
        initial={
            'corRFID'  : cor_rfid_funcao.corRFID ,
            'cod_cargo'  : cor_rfid_funcao.cod_cargo,   
        },
        cod_cargoID = cor_rfid_funcao.cod_cargo.id
    )
    
    context = {
        'form' : form,
        'title' : 'Edicao de Cor-Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    # IFTO Acess: Uma proposta de Controle de Acesso para o Instituto
    return render(request, "pages/corRfid/editarCorRfid.html", context)