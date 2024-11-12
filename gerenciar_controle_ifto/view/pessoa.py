from django.shortcuts import render, get_object_or_404
from gerenciar_controle_ifto.models import Pessoa,Papel_pessoa
from datetime import datetime
from django.http import HttpResponseRedirect
from gerenciar_controle_ifto.forms import EditarPessoaForm
from django.contrib.auth.decorators import login_required

def converterData(pessoas):
    for pessoa in pessoas:
        pessoa.data_nascimento = pessoa.data_nascimento.strftime("%d/%m/%Y")
        
    return pessoas

def calcularIdade(data_nascimento):
    dt = datetime.strptime(data_nascimento,"%Y-%m-%d")
    tdt = dt.timetuple()
    data_list = []

    for data in tdt:
        data_list.append(data)

    ano_nascimento = int(data_list[0])
    mes_nascimento = int(data_list[1])
    dia_nascimento = int(data_list[2])
    
    dia_atual = datetime.now().day
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    idade = (ano_atual - ano_nascimento)
    
    if (mes_nascimento < mes_atual):
        return idade
    else:
        if(mes_atual == mes_nascimento):
            if(dia_nascimento <= dia_atual):
                return idade
            else:
                return idade-1
        else:
            return idade-1


def cadastrarPessoa(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    funcoes = Papel_pessoa.objects.all()
    
    context = {
        'title' : 'Cadastro de Pessoa',
        'funcoes' : funcoes,
        'nome_usuario_logado' : nome_usuario
    }
    
    if request.method == 'POST':
        nome_pessoa = request.POST.get('nome_pessoa')
        sobrenome_completo_pessoa = request.POST.get('sobrenome_completo_pessoa')
        data_nascimento = request.POST.get('data_nascimento')
        cpf_pessoa = request.POST.get('cpf_pessoa')
        funcao_pessoa = int(request.POST.get('funcao_pessoa'))

        pessoa = Pessoa(nome = nome_pessoa, 
                        sobrenome = sobrenome_completo_pessoa, 
                        cpf=cpf_pessoa,
                        data_nascimento = data_nascimento,
                        idade = calcularIdade(data_nascimento),
                        cod_Papel_pessoa = Papel_pessoa.objects.get(pk=funcao_pessoa),
                        vinculado=False
                        )
        pessoa.save()
        
        return HttpResponseRedirect("/iftoAcess/listar/pessoa/")
        
    return render(request, 'pages/pessoa/cadastrarPessoa.html', context)

def listarPessoa(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username
    
    pessoas = Pessoa.objects.all()
    pessoas = converterData(pessoas)
    
    context = {
        'title' : 'Listagem de Pessoa',
        'pessoas' : pessoas,
        'nome_usuario_logado' : nome_usuario
    }
    return render(request, 'pages/pessoa/listarPessoa.html', context)

def editarPessoa(request, id):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.username

    pessoa = get_object_or_404(Pessoa, id=id)

    if request.method == 'POST':
        form = EditarPessoaForm(request.POST)

        if form.is_valid():
            pessoa.nome = form.cleaned_data['nome']
            pessoa.sobrenome = form.cleaned_data['sobrenome']
            pessoa.cpf = form.cleaned_data['cpf']
            pessoa.cod_Papel_pessoa = form.cleaned_data['cod_Papel_pessoa']
            pessoa.data_nascimento = form.cleaned_data['data_nascimento']
            pessoa.save()
            
            return HttpResponseRedirect('/iftoAcess/listar/pessoa/')

        context = {
        'form' : form,
        'title' : 'Edicao de Pessoa',
        'nome_usuario_logado' : nome_usuario
        }
        return render(request, 'pages/pessoa/editarPessoa.html', context)    
    
    form = EditarPessoaForm(
        initial = {
            'nome' : pessoa.nome,
            'sobrenome' : pessoa.sobrenome,
            'cpf' : pessoa.cpf,
            'cod_Papel_pessoa' : pessoa.cod_Papel_pessoa,
            'data_nascimento' : pessoa.data_nascimento
        },
        cod_cargoID = pessoa.cod_Papel_pessoa.id
    )
    
    context = {
        'form' : form,
        'title' : 'Edicao de Pessoa',
        'nome_usuario_logado' : nome_usuario
    }
    return render(request, 'pages/pessoa/editarPessoa.html', context)