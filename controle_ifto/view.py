import mysql.connector as mysql
from datetime import datetime

import json

def validarAcesso(value_rfid):

    cursor,conexao_mysql = conexao()
    command_sql = """SELECT P.id,P.nome, P.sobrenome, rfid.tag_rfid_value FROM gerenciar_controle_ifto_pessoa AS P
                    INNER JOIN gerenciar_controle_ifto_rfid as Rfid ON P.id = Rfid.id
                    WHERE rfid.rfid_value = %s;
                    """
    values = (value_rfid,)
    mysql_resultado = None

    try:
        cursor.execute(command_sql,values)
        mysql_resultado = cursor.fetchall()

    except Exception as ex:
        print(f"Erro: {ex}")

    finally:
        conexao_mysql.close()
        cursor.close()

    for result in mysql_resultado:
        print(result)


def cadHistoricoAceso(cod_rfid,cod_pessoa,funcao_pessoadata_acesso):
    
    cursor,conexao_mysql = conexao()
    command_sql = """ INSERT INTO gerenciar_controle_ifto_historico_acesso_campus(cod_rfid_id, cod_pessoa_id, funcao_pessoa_id, data_acesso) 
                       VALUES (%s,%s,%s,%s)
                  """

    values = (cod_rfid,cod_pessoa,funcao_pessoadata_acesso,)
    
    try:
        cursor.execute(command_sql,values)
        conexao_mysql.commit()

    except Exception as ex:
        print(f"Erro: {ex}")

    finally:
        conexao_mysql.close()
        cursor.close()

def cadPessoa(nome, sobrenome,cpf,data_nasc, idade, vinculado):

    cursor,conexao_mysql = conexao()

    command_sql = "INSERT INTO gerenciar_controle_ifto_pessoa(nome, sobrenome, cpf, data_nascimento,idade,vinculado) VALUE(%s,%s,%s,%s,%s,%s)"
    val = (nome,sobrenome,cpf,data_nasc,idade,vinculado)

    try:
        cursor.execute(command_sql, val)
        conexao_mysql.commit()
        print("Pessoa salva")

    except Exception as ex:
        print(f"Erro: {ex}")
        conexao_mysql.close()
        cursor.close()

#def buscarRfidVinculado():
    
        
#def histori():
    
        
def cadRFID(rfid):
    
    cursor,conexao_mysql = conexao()
    
    command_sql = "INSERT INTO rfid(rfid_value) VALUE(%s)"
    val = (rfid,)
       
    try:
        cursor.execute(command_sql, val)
        conexao_mysql.commit()
        print("RFID salvo")

    except Exception as ex:
        print(f"Erro: {ex}")
        conexao_mysql.close()
        cursor.close()
        
def cadPapelPessoa(papel_pessoa):

    cursor,conexao_mysql = conexao()

    command_sql = "INSERT INTO Papel_pessoa(papel_pessoa) VALUE(%s)"
    val = (papel_pessoa,)
       
    try:
        cursor.execute(command_sql, val)
        conexao_mysql.commit()
        print("Papel_pessoa salvo")

    except Exception as ex:
        print(f"Erro: {ex}")
        conexao_mysql.close()
        cursor.close()


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
    
    #if(cursor.execute):
    #    print("Conexão feita")
    #    conexao_mysql.close()
    #else:
    #    print("Deu pau kkkk")
    
    return cursor,conexao_mysql
               

def lerJSON():
    with open("controle_ifto/dados_conexao.json",encoding='utf-8') as atributo_conexao:
        dados = json.load(atributo_conexao)
        
    return dados

#rfid = "2E 4V VF YI"


#nome_rfids = [
#]
#
#for nome_rfid in nome_rfids:
#    cadPessoa(nome_rfid['nome'],nome_rfid['rfid'])

#rfids = ["W2 F4 5A QQ", "14 K8 80 00", "12 76 9A SX", "1C 5A 66 7Y", "2W 9U 7A PL", "Z3 R1 DA WY", "2E 4V VF YI"]
#
#for rfid in rfids:
#    cadRFID(rfid)

#papel_pessoa = ["Tecnico Administrativo"]
#
#for papel in papel_pessoa:
#    cadPapelPessoa(papel)

#rfid = "1C 5A 66 7Y"
#validarAcesso(rfid)

#nome = "Daniely"
#sobrenome = "Santos"
#cpf = "845.174.449-93"
#data_nasc = '2004-09-15'
#idade = 20
#vinculado = False
#
#cadPessoa(nome, sobrenome,cpf,data_nasc, idade, vinculado)