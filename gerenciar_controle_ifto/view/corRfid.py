from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from gerenciar_controle_ifto.models import CorRFID_Funcao, Papel_pessoa
from gerenciar_controle_ifto.formularios.CorRfidForm import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/iftoAcess/login/')
def cadastrarCorRfid(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
    
    if request.method == 'POST':
        form = CadastrarCorRfidForm(request.POST)
    
        if form.is_valid():
            cod_cargo = form.cleaned_data['cod_cargo']
            
            corRfid = CorRFID_Funcao(corRFID = form.cleaned_data['corRFID'],
                                     cod_cargo = cod_cargo
                                    )
            corRfid.save()
            
            funcao_a_vincular = Papel_pessoa.objects.get(pk=cod_cargo.id)
            funcao_a_vincular.vinculado_corRfid = True
            funcao_a_vincular.save()

            # Neste trecho de codigo ser'a executado, caso venha ser feito a alteracao de funcao relacionado a cor
            # na qual sera realizado a alteracao do status de 'vinculado_corRfid'
            return HttpResponseRedirect('/iftoAcess/listar/corRfid/')

        context = {
            'form' : form,
            'title' : 'Cadastro de Cor-Rfid',
            'usuario_staff_atual':request.user.is_staff,
            'nome_usuario_logado' : nome_usuario
        }
        return render(request,'pages/corRfid/editarCorRfid.html', context)


    form = CadastrarCorRfidForm()
       
    context = {
            'form' : form,
            'title' : 'Cadastro de Cor-Rfid',
            'usuario_staff_atual':request.user.is_staff,
            'nome_usuario_logado' : nome_usuario
        }
    return render(request,'pages/corRfid/editarCorRfid.html', context)
    

        
@login_required(login_url='/iftoAcess/login/')
def listarCorRfid(request):

    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
        
    if request.method == "POST":
        form = BuscarCorRfidForm(request.POST)
       
        if form.is_valid():
            campo = form.cleaned_data['campo']
           
            if campo==None or campo=="":
               
                coresRfid = CorRFID_Funcao.objects.all()
                context = {
                    'title' : 'Listagem de Cor-Rfid',
                    'form' : form,
                    'usuario_staff_atual':request.user.is_staff,
                    'coresRfid' : coresRfid,
                    'nome_usuario_logado' : nome_usuario
                }
                return render(request, "pages/corRfid/listarCorRfid.html", context)


            coresRfid = CorRFID_Funcao.objects.filter(corRFID__icontains=campo)

            if(len(coresRfid)<=0):
                funcao = Papel_pessoa.objects.filter(descricao__icontains=campo).first()
                coresRfid = CorRFID_Funcao.objects.filter(cod_cargo=funcao)

            context = {
                    'title' : 'Listagem de Cor-Rfid',
                    'form' : form,
                    'usuario_staff_atual':request.user.is_staff,
                    'coresRfid' : coresRfid,
                    'nome_usuario_logado' : nome_usuario
                }
            return render(request, "pages/corRfid/listarCorRfid.html", context)
    
    form = BuscarCorRfidForm()
    coresRfid = CorRFID_Funcao.objects.all()

    context = {
        'title' : 'Listagem de Cor-Rfid',
        'form' : form,
        'usuario_staff_atual':request.user.is_staff,
        'coresRfid' : coresRfid,
        'nome_usuario_logado' : nome_usuario
    }

    return render(request, "pages/corRfid/listarCorRfid.html", context)

@login_required(login_url='/iftoAcess/login/')
def editarCorRfid(request, id):

    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
    
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
            'title' : 'Edicão de Cor-Rfid',
            'usuario_staff_atual':request.user.is_staff,
            'nome_usuario_logado' : nome_usuario
        }
        return render(request,'pages/corRfid/editarCorRfid.html', context)


    form = EditarCorRfidForm(
        initial={
            'id':corRfid_funcao.id,
            'corRFID': corRfid_funcao.corRFID,
            'cod_cargo': corRfid_funcao.cod_cargo
        },
        cod_cargoID = corRfid_funcao.id
    )
       
    context = {
            'form' : form,
            'corRfid_funcao' : corRfid_funcao,
            'title' : 'Edicão de Cor-Rfid',
            'usuario_staff_atual':request.user.is_staff,
            'nome_usuario_logado' : 'Rangerson'
        }
    return render(request,'pages/corRfid/editarCorRfid.html', context)