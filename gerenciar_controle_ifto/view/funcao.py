from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from gerenciar_controle_ifto.models import Papel_pessoa
from gerenciar_controle_ifto.forms import EditarFuncaoForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/iftoAcess/login/')
def cadastrarFuncao(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    context = {
        'title' : 'Cadastro de Função',
        'nome_usuario_logado' : nome_usuario
    }
    
    if request.method == 'POST':
        descricao = request.POST.get('descricao_funcao')
        
        if descricao == None:
            return HttpResponse("Campo 'Descrição' obrigatório")
        
        funcao = Papel_pessoa(descricao=descricao,
                              vinculado_corRfid = False
                              )
        funcao.save()
        return HttpResponseRedirect('/iftoAcess/listar/funcao/')
    
    return render(request, "pages/funcao/cadastrarFuncao.html", context)

@login_required(login_url='/iftoAcess/login/')
def editarFuncao(request, id):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username

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
        'title' : 'Edicao de Funcao',
        'nome_usuario_logado' : nome_usuario
        }
        return render(request, 'pages/funcao/editarFuncao.html', context)


    form = EditarFuncaoForm(
        initial={
            'funcao' : funcao.descricao
        }
    )
    
    context = {
        'form' : form,
        'funcao' : funcao,
        'title' : 'Edicao de Funcao',
        'nome_usuario_logado' : nome_usuario
    }
    
    return render(request, 'pages/funcao/editarFuncao.html', context)
    
@login_required(login_url='/iftoAcess/login/')
def listarFuncao(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    funcoes = Papel_pessoa.objects.all()
    
    context = {
        'title' : 'Listagem de Função',
        'funcoes' : funcoes,
        'nome_usuario_logado' : nome_usuario
    }    
    return render(request, "pages/funcao/listarFuncao.html", context)