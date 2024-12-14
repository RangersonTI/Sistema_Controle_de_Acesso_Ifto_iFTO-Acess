from django.shortcuts import render, get_object_or_404
from gerenciar_controle_ifto.models import Pessoa,Papel_pessoa
from datetime import datetime
from django.http import HttpResponseRedirect
from gerenciar_controle_ifto.formularios.PessoaForm import *
from django.db.models import Q
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

@login_required(login_url='/iftoAccess/login/')
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

            return HttpResponseRedirect('/iftoAccess/listar/pessoa/')

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


@login_required(login_url='/iftoAccess/login/')
def listarPessoa(request):

    if request.user.is_authenticated:
        nome_usuario = request.user.first_name
    
    
    if request.method == "POST":
        form = BuscarPessoaForm(request.POST)
        
        if form.is_valid():
            campo = form.cleaned_data['campo']
            
            if (campo == "" or campo == None):
                pessoas = Pessoa.objects.all()
                pessoas = converterData(pessoas)

                context = {
                    'title' : 'Listagem de Pessoa',
                    'form' :form,
                    'usuario_staff_atual':request.user.is_staff,
                    'pessoas' : pessoas,
                    'nome_usuario_logado' : nome_usuario
                }
                return render(request, 'pages/pessoa/listarPessoa.html', context)
            
            pessoas = Pessoa.objects.filter(nome__icontains=campo)
            print(len(pessoas))
            
            if len(pessoas) <=0:
                pessoas = Pessoa.objects.filter(sobrenome__icontains=campo)

            if len(pessoas) <=0:
                pessoas = Pessoa.objects.filter(cpf=campo)
                
            pessoas = converterData(pessoas)

            context = {
                'title' : 'Listagem de Pessoa',
                'form' :form,
                'usuario_staff_atual':request.user.is_staff,
                'pessoas' : pessoas,
                'nome_usuario_logado' : nome_usuario
            }
            return render(request, 'pages/pessoa/listarPessoa.html', context)
                
    form = BuscarPessoaForm()
    
    pessoas = Pessoa.objects.all()
    pessoas = converterData(pessoas)
    
    context = {
        'title' : 'Listagem de Pessoa',
        'form' :form,
        'usuario_staff_atual':request.user.is_staff,
        'pessoas' : pessoas,
        'nome_usuario_logado' : nome_usuario
    }
    return render(request, 'pages/pessoa/listarPessoa.html', context)

@login_required(login_url='/iftoAccess/login/')
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
            pessoa.save()

            return HttpResponseRedirect('/iftoAccess/listar/pessoa/')

        context = {
            'form' : form,
            'title' : 'Edicão de Pessoa',
            'usuario_staff_atual':request.user.is_staff,
            'nome_usuario_logado' : nome_usuario
        }
        return render(request, 'pages/pessoa/editarPessoa.html', context)    
    
    tdt = (pessoa.data_nascimento).timetuple()
    data_tdt = []
    
    print(type(tdt))
    
    for data in tdt:
        data_tdt.append(data)
        
        
    if (int(data_tdt[1]) < 10):
        data_nascimento = f"{data_tdt[0]}-0"+f"{data_tdt[1]}-"+f"{data_tdt[2]}"
    else:
        data_nascimento = f"{data_tdt[2]}-"+f"{data_tdt[1]}-"+f"{data_tdt[0]}"
        
    print(data_nascimento)

    form = EditarPessoaForm(
        initial = {
            'id' : int(pessoa.id),
            'nome' : pessoa.nome,
            'sobrenome' : pessoa.sobrenome,
            'cpf' : pessoa.cpf,
            'cod_Papel_pessoa' : pessoa.cod_Papel_pessoa,
            'data_nascimento' : data_nascimento
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