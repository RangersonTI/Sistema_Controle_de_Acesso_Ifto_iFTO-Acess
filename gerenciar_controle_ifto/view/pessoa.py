from django.shortcuts import render, get_object_or_404
from gerenciar_controle_ifto.models import Pessoa,Papel_pessoa
from datetime import datetime
from django.http import HttpResponseRedirect
from gerenciar_controle_ifto.formularios.PessoaForm import *
from django.contrib.auth.decorators import login_required

def converterData(pessoas):
    for pessoa in pessoas:
        pessoa.data_nascimento = pessoa.data_nascimento.strftime("%d/%m/%Y")
        
    return pessoas

def calcularIdade(data_nascimento):
    print(data_nascimento)
    
    #dt = datetime.strptime(data_nascimento,"%Y-%m-%d")
    tdt = data_nascimento.timetuple()
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

@login_required(login_url='/iftoAcess/login/')
def cadastrarPessoa(request):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
    

    if request.method == 'POST':
        form = CadastrarPessoaForm(request.POST)

        if form.is_valid():
            pessoa = Pessoa(nome = form.cleaned_data['nome'], 
                        sobrenome = form.cleaned_data['sobrenome'], 
                        cpf=form.cleaned_data['cpf'],
                        data_nascimento = form.cleaned_data['data_nascimento'],
                        idade = calcularIdade(form.cleaned_data['data_nascimento']),
                        cod_Papel_pessoa = form.cleaned_data['cod_Papel_pessoa'],
                        vinculado=False
                        )
            pessoa.save()

            return HttpResponseRedirect('/iftoAcess/listar/pessoa/')

        context = {
            'form' : form,
            'title' : 'Cadastro de Pessoa',
            'usuario_staff_atual':request.user.is_staff,
            'nome_usuario_logado' : nome_usuario
        }
        return render(request, 'pages/pessoa/cadastrarPessoa.html', context)    

    form = CadastrarPessoaForm()
    
    context = {
        'form' : form,
        'title' : 'Cadastro de Pessoa',
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
    }
    return render(request, 'pages/pessoa/cadastrarPessoa.html', context)


@login_required(login_url='/iftoAcess/login/')
def listarPessoa(request):

    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
    
    pessoas = Pessoa.objects.all()
    pessoas = converterData(pessoas)
    
    context = {
        'title' : 'Listagem de Pessoa',
        'usuario_staff_atual':request.user.is_staff,
        'pessoas' : pessoas,
        'nome_usuario_logado' : nome_usuario
    }
    return render(request, 'pages/pessoa/listarPessoa.html', context)

@login_required(login_url='/iftoAcess/login/')
def editarPessoa(request, id):
    
    if request.user.is_authenticated:
        nome_usuario = request.user.first_name

    pessoa = get_object_or_404(Pessoa, id=id)

    if request.method == 'POST':
        form = EditarPessoaForm(request.POST)

        if form.is_valid():
            pessoa.nome = form.cleaned_data['nome']
            pessoa.sobrenome = form.cleaned_data['sobrenome']
            pessoa.cpf = form.cleaned_data['cpf']
            pessoa.data_nascimento = form.cleaned_data['data_nascimento']
            if pessoa.vinculado == False:
                pessoa.cod_Papel_pessoa = form.cleaned_data['cod_Papel_pessoa']
            print(pessoa.data_nascimento)
            pessoa.save()

            return HttpResponseRedirect('/iftoAcess/listar/pessoa/')

        context = {
            'form' : form,
            'title' : 'Edicão de Pessoa',
            'usuario_staff_atual':request.user.is_staff,
            'nome_usuario_logado' : nome_usuario
        }
        return render(request, 'pages/pessoa/editarPessoa.html', context)    

    form = EditarPessoaForm(
        initial = {
            'id' : int(pessoa.id),
            'nome' : pessoa.nome,
            'sobrenome' : pessoa.sobrenome,
            'cpf' : pessoa.cpf,
            'cod_Papel_pessoa' : pessoa.cod_Papel_pessoa,
            'data_nascimento' : datetime.strptime(str(pessoa.data_nascimento),'%Y-%m-%d')
        },
        cod_cargoID = pessoa.cod_Papel_pessoa.id,
        vinculado = pessoa.vinculado,
    )
    
    context = {
        'form' : form,
        'title' : 'Edicão de Pessoa',
        'usuario_staff_atual':request.user.is_staff,
        'nome_usuario_logado' : nome_usuario
    }
    return render(request, 'pages/pessoa/editarPessoa.html', context)