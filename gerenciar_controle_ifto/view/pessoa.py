from django.shortcuts import render
from gerenciar_controle_ifto.models import Pessoa,Papel_pessoa
from datetime import datetime

def calcularIdade(data_nascimento):
    dt = datetime.strptime(data_nascimento,"%Y-%m-%d")
    tdt = dt.timetuple()
    data_list = []

    for data in tdt:
        data_list.append(data)

    print(data_list)

    ano_nascimento = data_list[0]
    mes_nascimento = data_list[1]
    dia_nascimento = data_list[2]

    idade = (int(datetime.year) - int(ano_nascimento))
    
    if (mes_nascimento < datetime.month):
        return idade
    else:
        if(datetime.month == mes_nascimento):
            if(dia_nascimento <= datetime.day):
                return idade
            else:
                return idade-1
        else:
            return idade-1


def cadastrarPessoa(request):
    funcoes = Papel_pessoa.objects.all()
    
    context = {
        'title' : 'Cadastro de Pessoa',
        'funcoes' : funcoes,
        'nome_usuario_logado' : 'Rangerson'
    }
    
    if request.method == 'POST':
        nome_pessoa = request.POST.get('nome_pessoa')
        sobrenome_completo_pessoa = request.POST.get('sobrenome_completo_pessoa')
        data_nascimento = request.POST.get('data_nascimento')
        cpf_pessoa = request.POST.get('cpf_pessoa')
        funcao_pessoa = request.POST.get('funcao_pessoa')

        pessoa = Pessoa(nome = nome_pessoa, 
                        sobrenome = sobrenome_completo_pessoa, 
                        cpf=cpf_pessoa,
                        data_nascimento = data_nascimento,
                        idade = calcularIdade(data_nascimento),
                        cod_Papel_pessoa = funcao_pessoa
                        )
        pessoa.save()
        
    return render(request, 'pages/pessoa/cadastrarPessoa.html', context)

def listarPessoa(request):
    
    context = {
        'title' : 'Listagem de Pessoa',
        'nome_usuario_logado' : 'Rangerson'
    }
    return render(request, 'pages/pessoa/listarPessoa.html', context)