import mysql.connector as mysql
from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ValidarAcesso(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            value_rfid = data['tag_rfid_value']
            cod_esp32 = data['cod_esp32']

        except json.JSONDecodeError as ex:
            return JsonResponse({"Status" : "Error de decodificacao :("})

        #Senha criptografada em SHA-512, depois com esse valor em mão, repetir o processo mais 4 vezes chegando assim ao resultado
        # Senha é control_acess_ifto_permission_true

        if(cod_esp32 == '3FFB4E290515F69B245D02B36DDBCF186C52A1399D3FA0B4F4B97D386D009FFAE93CDD0A68570CEADE64C6C9E36EA958C23A568A356A18EDDC7084E67F7A140B'):
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

            if mysql_resultado:
                cod_pessoa = mysql_resultado[0][0]                      # Referente à coluna Pessoa.id
                cod_funcao_pessoa = mysql_resultado[0][3]               # Referente à coluna Pessoa.cod_Papel_pessoa_id
                cod_rfid = mysql_resultado[0][4]                        # Referente à coluna Pessoa.cod_Rfid_id

                result = CadastroHistoricoAcesso(cod_pessoa, cod_rfid, cod_funcao_pessoa)
                return JsonResponse({"Status" : result})
            else:
                if(VerificarRFID(value_rfid)):
                    return JsonResponse({"Status" : "rfid_unidentified"})
                else:
                    return JsonResponse({"Status" : "rfid_not_found"})

        return render(request, 'no_acess.html', {'title': 'Acesso Negado', 'mensagem':'Você não possui autorização para acessar esta página'})
    return render(request, 'no_acess.html', {'title': 'Acesso Negado', 'mensagem':'Você não possui autorização para acessar esta página'})

"""
    Codigos de Status para a Validacao e Cadastro de Acesso
    
    save_Acess : Historico de acesso salvo... Liberado :)
    erro_to_save_acess : Erro ao registrar o acesso
    rfid_unidentified: RFID nao vinculado
    rfid_not_found : RFID invalido

"""

def VerificarRFID(value_rfid):
    
    cursor,conexao_mysql = conexao()
    command_sql = "SELECT * FROM gerenciar_controle_ifto_rfid WHERE tag_rfid_value = %s;"
    values = (value_rfid,)

    try:
        cursor.execute(command_sql,values)
        mysql_resultado = cursor.fetchall()

    except Exception as ex:
        print(f"Erro: {ex}")

    finally:
        conexao_mysql.close()
        cursor.close()

    if mysql_resultado:
        return True
    
    return False

def CadastroHistoricoAcesso(cod_pessoa,cod_rfid,cod_funcao_pessoa):

    cursor,conexao_mysql = conexao()
    command_sql = """ INSERT INTO gerenciar_controle_ifto_historico_acesso_campus(cod_rfid_id, cod_pessoa_id, funcao_pessoa_id, data_acesso)
                       VALUES (%s,%s,%s,now());
                  """

    values = (cod_rfid,cod_pessoa,cod_funcao_pessoa)

    try:
        cursor.execute(command_sql,values)
        conexao_mysql.commit()

    except Exception as ex:
        return(f"erro_to_save_acess")

    finally:
        conexao_mysql.close()
        cursor.close()

    return("save_acess")

def conexao():

    dados = lerJSON()
    try:
        conexao_mysql = mysql.connect(
            host= dados['host'],
            user= dados['user'],
            port= dados['port'],
            password= dados['password'],
            database= dados['database'],
        )
    except Exception as ex:
        print(ex)

    cursor = conexao_mysql.cursor()
    return cursor,conexao_mysql

def lerJSON():
    try:
        with open("controle_ifto/dados_conexao.json",encoding='utf-8') as atributo_conexao:
            return json.load(atributo_conexao)
    except:
        print("O arquivo JSON de configuração não foi encontrado. Por favor verficar se o arquivo existe")
