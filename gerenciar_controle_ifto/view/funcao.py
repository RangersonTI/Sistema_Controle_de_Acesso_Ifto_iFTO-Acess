from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from gerenciar_controle_ifto.models import Papel_pessoa
from gerenciar_controle_ifto.forms import EditarFuncaoForm

def cadastrarFuncao(request):
    
    context = {
        'title' : 'Cadastro de Função',
        'nome_usuario_logado' : 'Rangerson'
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

def editarFuncao(request, id):

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
        'nome_usuario_logado' : 'Rangerson'
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
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/funcao/editarFuncao.html', context)
    

def listarFuncao(request):
    
    funcoes = Papel_pessoa.objects.all()
    
    context = {
        'title' : 'Listagem de Função',
        'funcoes' : funcoes,
        'nome_usuario_logado' : 'Rangerson'
    }    
    return render(request, "pages/funcao/listarFuncao.html", context)