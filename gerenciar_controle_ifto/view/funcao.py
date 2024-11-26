from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from gerenciar_controle_ifto.models import Papel_pessoa
from gerenciar_controle_ifto.formularios.FuncaoForm import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/iftoAcess/login/')
def cadastrarFuncao(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

    if request.method == 'POST':
        form = CadastrarFuncaoForm(request.POST)

        if form.is_valid():
            funcao = Papel_pessoa(descricao=form.cleaned_data['funcao'],
                              vinculado_corRfid = False
                              )
            funcao.save()
            return HttpResponseRedirect('/iftoAcess/listar/funcao')
        
        context = {
        'form' : form,
        'title' : 'Cadastro de Função',
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
        }
        return render(request, 'pages/funcao/editarFuncao.html', context)


    form = CadastrarFuncaoForm()

    context = {
        'form' : form,
        'title' : 'Cadastro de Função',
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/funcao/editarFuncao.html', context)


@login_required(login_url='/iftoAcess/login/')
def editarFuncao(request, id):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

    funcao = get_object_or_404(Papel_pessoa, id=id)

    if request.method == 'POST':
        form = EditarFuncaoForm(request.POST)

        if form.is_valid():
            funcao.descricao = form.cleaned_data['funcao']
            funcao.save()
            return HttpResponseRedirect('/iftoAcess/listar/funcao')

        context = {
        'form' : form,
        'funcao' : funcao,
        'title' : 'Edicão de Função',
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
        }
        return render(request, 'pages/funcao/editarFuncao.html', context)


    form = EditarFuncaoForm(
        initial={
            'id' : funcao.id,
            'funcao' : funcao.descricao
        }
    )

    context = {
        'form' : form,
        'funcao' : funcao,
        'title' : 'Edicão de Função',
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
    }

    return render(request, 'pages/funcao/editarFuncao.html', context)

@login_required(login_url='/iftoAcess/login/')
def listarFuncao(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
        
    if request.method == "POST":
        form = BuscarFuncaoForm(request.POST)
        
        if form.is_valid():
            campo = form.cleaned_data['campo']
            
            if campo == None or campo == "":
                funcoes = Papel_pessoa.objects.all()
                context = {
                    'title' : 'Listagem de Função',
                    'form': form,
                    'usuario_staff_atual':request.user.is_staff,
                    'funcoes' : funcoes,
                    'nome_usuario_logado' : nome_usuario
                }    
                return render(request, "pages/funcao/listarFuncao.html", context)
            
            funcoes = Papel_pessoa.objects.filter(descricao__icontains=campo)
            context = {
                    'title' : 'Listagem de Função',
                    'form': form,
                    'usuario_staff_atual':request.user.is_staff,
                    'funcoes' : funcoes,
                    'nome_usuario_logado' : nome_usuario
                }    
            return render(request, "pages/funcao/listarFuncao.html", context)

    form = BuscarFuncaoForm()
    
    funcoes = Papel_pessoa.objects.all()
    context = {
        'title' : 'Listagem de Função',
        'form': form,
        'usuario_staff_atual':request.user.is_staff,
        'funcoes' : funcoes,
        'nome_usuario_logado' : nome_usuario
    }    
    return render(request, "pages/funcao/listarFuncao.html", context)