import mysql.connector as mysql
import json

def validarAcesso(request):
    return

def cadHistoricoAceso(request):
    return

def conexao():
    
    dados = lerJSON()
    conexao_mysql = mysql.connect(
        host= dados['host'],
        user= dados['user'],
        port= dados['port'],
        password= dados['password'],
        database= dados['database'],
    )
    
    cursor = conexao_mysql.cursor()
    
    if(cursor.execute):
        print("Conexão feita")
        conexao_mysql.close()
    else:
        print("Deu pau kkkk")
               

def lerJSON():
    with open("controle_ifto/dados_conexao.json",encoding='utf-8') as atributo_conexao:
        dados = json.load(atributo_conexao)
        
    return dados