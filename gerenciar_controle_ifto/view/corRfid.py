from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from gerenciar_controle_ifto.models import CorRFID_Funcao, Papel_pessoa
from gerenciar_controle_ifto.forms import EditarCorRfidForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/iftoAcess/login/')
def cadastrarCorRfid(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    funcoes = Papel_pessoa.objects.filter(vinculado_corRfid=False)

    context = {
        'title' : 'Cadastro de Cor-Rfid',
        'nome_usuario_logado' : nome_usuario,
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

@login_required(login_url='/iftoAcess/login/')
def listarCorRfid(request):

    if request.user.is_authenticated:
        nome_usuario = request.user.username
        
    coresRfid = CorRFID_Funcao.objects.all()

    context = {
        'title' : 'Listagem de Cor-Rfid',
        'coresRfid' : coresRfid,
        'nome_usuario_logado' : nome_usuario
    }

    return render(request, "pages/corRfid/listarCorRfid.html", context)

@login_required(login_url='/iftoAcess/login/')
def editarCorRfid(request, id):

    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    corRfid_funcao = get_object_or_404(CorRFID_Funcao,id=id)
    
    if request.method == 'POST':
        form = EditarCorRfidForm(request.POST)
    
        if form.is_valid():
            corRfid_funcao.corRFID = form.cleaned_data['corRFID']
            corRfid_funcao.cod_cargo = form.cleaned_data['cod_cargo']

            corRfid_funcao_anterior = CorRFID_Funcao.objects.get(pk=id)

            # Neste trecho de codigo ser'a executado, caso venha ser feito a alteracao de funcao relacionado a cor
            # na qual sera realizado a alteracao do status de 'vinculado_corRfid'
            
            if not(corRfid_funcao.cod_cargo.id == corRfid_funcao_anterior.cod_cargo.id):

                edit_funcao_anterior = Papel_pessoa.objects.get(pk=corRfid_funcao_anterior.cod_cargo.id)
                edit_funcao_anterior.vinculado_corRfid = False
                edit_funcao_anterior.save()

                edit_funcao_atual = Papel_pessoa.objects.get(pk=corRfid_funcao.cod_cargo.id)
                edit_funcao_atual.vinculado_corRfid = True
                edit_funcao_atual.save()

            corRfid_funcao.save()
            return HttpResponseRedirect('/iftoAcess/listar/corRfid/')

        context = {
            'form' : form,
            'title' : 'Edicao de Cor-Rfid',
            'nome_usuario_logado' : nome_usuario
        }
        return render(request,'pages/corRfid/editarCorRfid.html', context)


    form = EditarCorRfidForm(
        initial={
            'corRFID': corRfid_funcao.corRFID,
            'cod_cargo': corRfid_funcao.cod_cargo
        },
        cod_cargoID = corRfid_funcao.id
    )
       
    context = {
            'form' : form,
            'corRfid_funcao' : corRfid_funcao,
            'title' : 'Edicao de Cor-Rfid',
            'nome_usuario_logado' : 'Rangerson'
        }
    return render(request,'pages/corRfid/editarCorRfid.html', context)
    # IFTO Acess: Uma proposta de Controle de Acesso para o Instituto