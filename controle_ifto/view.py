import mysql.connector as mysql
from datetime import datetime

import json

def validarAcesso(value_rfid):

    cursor,conexao_mysql = conexao()
    command_sql = """ SELECT P.id,P.nome, P.sobrenome, P.cod_Papel_pessoa_id, P.cod_Rfid_id, Rfid.tag_rfid_value FROM gerenciar_controle_ifto_pessoa AS P
                      INNER JOIN gerenciar_controle_ifto_rfid as Rfid ON P.cod_Rfid_id = Rfid.id
                      WHERE Rfid.tag_rfid_value = %s;
                    """
    values = (value_rfid,)


    try:
        cursor.execute(command_sql,values)
        mysql_resultado = cursor.fetchall()

    except Exception as ex:
        print(f"Erro: {ex}")

    finally:
        conexao_mysql.close()
        cursor.close()
    print(mysql_resultado)

    if mysql_resultado:
        if(value_rfid == mysql_resultado[0][5]):
            cod_pessoa = mysql_resultado[0][0]                      # Referente à coluna Pessoa.id
            cod_funcao_pessoa = mysql_resultado[0][3]               # Referente à coluna Pessoa.cod_Papel_pessoa_id
            cod_rfid = mysql_resultado[0][4]                        # Referente à coluna Pessoa.cod_Rfid_id
            #data_acesso = datetime.now()
            #print(data_acesso)

            cadastroHistoricoAcesso(cod_pessoa, cod_funcao_pessoa, cod_rfid)
    else:
        if(VerificarRFID(value_rfid)):
            print("RFID não vinculado")
        else:
            print("RFID inválido")


def VerificarRFID(value_rfid):
    
    cursor,conexao_mysql = conexao()
    command_sql = "SELECT * FROM gerenciar_contrle_ifto_rfid WHERE tag_value_rfid = %s;"
    values = (value_rfid)
    
    try:
        cursor.execute(command_sql,values)
        mysql_resultado = cursor.fetchall()

    except Exception as ex:
        print(f"Erro: {ex}")

    finally:
        conexao_mysql.close()
        cursor.close()

    print(mysql_resultado)

    if(mysql_resultado):
        return True
    
    return False

def cadastroHistoricoAcesso(cod_pessoa,cod_rfid,cod_funcao_pessoa):
    
    cursor,conexao_mysql = conexao()
    command_sql = """ INSERT INTO gerenciar_controle_ifto_historico_acesso_campus(cod_rfid_id, cod_pessoa_id, funcao_pessoa_id, data_acesso)
                       VALUES (%s,%s,%s,now());
                  """

    values = (cod_rfid,cod_pessoa,cod_funcao_pessoa)
    
    try:
        cursor.execute(command_sql,values)
        conexao_mysql.commit()

    except Exception as ex:
        print(f"Erro de cad_Historico: {ex}")

    finally:
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
    
    return cursor,conexao_mysql

def lerJSON():
    with open("controle_ifto/dados_conexao.json",encoding='utf-8') as atributo_conexao:
        dados = json.load(atributo_conexao)
        
    return dados

#rfid = "A4 R5 TT 12"
#
#validarAcesso(rfid)
















#def cadPessoa(nome, sobrenome,cpf,data_nasc, idade, vinculado):
#
#    cursor,conexao_mysql = conexao()
#
#    command_sql = "INSERT INTO gerenciar_controle_ifto_pessoa(nome, sobrenome, cpf, data_nascimento,idade,vinculado) VALUE(%s,%s,%s,%s,%s,%s)"
#    val = (nome,sobrenome,cpf,data_nasc,idade,vinculado)
#
#    try:
#        cursor.execute(command_sql, val)
#        conexao_mysql.commit()
#        print("Pessoa salva")
#
#    except Exception as ex:
#        print(f"Erro: {ex}")
#        conexao_mysql.close()
#        cursor.close()

#def buscarRfidVinculado():
    
        
#def histori():
    
        
#def cadRFID(rfid):
#    
#    cursor,conexao_mysql = conexao()
#    
#    command_sql = "INSERT INTO rfid(rfid_value) VALUE(%s)"
#    val = (rfid,)
#       
#    try:
#        cursor.execute(command_sql, val)
#        conexao_mysql.commit()
#        print("RFID salvo")
#
#    except Exception as ex:
#        print(f"Erro: {ex}")
#        conexao_mysql.close()
#        cursor.close()
#        
#def cadPapelPessoa(papel_pessoa):
#
#    cursor,conexao_mysql = conexao()
#
#    command_sql = "INSERT INTO Papel_pessoa(papel_pessoa) VALUE(%s)"
#    val = (papel_pessoa,)
#       
#    try:
#        cursor.execute(command_sql, val)
#        conexao_mysql.commit()
#        print("Papel_pessoa salvo")
#
#    except Exception as ex:
#        print(f"Erro: {ex}")
#        conexao_mysql.close()
#        cursor.close()



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

