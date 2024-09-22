import mysql.connector as mysql
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ValidarAcesso(request):
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            value_rfid = data['tag_rfid_value']
            cod_esp32 = data['cod_esp32']
            print(f"Dados: {value_rfid} e {cod_esp32}")
            
        except json.JSONDecodeError as ex:
            print(f"Erro: {ex}")
            return JsonResponse({"Status" : "Nao deu :("})

        if(cod_esp32 == 'control_acess_ifto_permission_true'):
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

                print(mysql_resultado[0][0])
                print(mysql_resultado[0][4])
                print(mysql_resultado[0][3])

                result = CadastroHistoricoAcesso(cod_pessoa, cod_rfid, cod_funcao_pessoa)
                return JsonResponse({"Status" : result})
            else:
                if(VerificarRFID(value_rfid)):
                    return JsonResponse({"Status" : "rfid_unidentified"})
                else:
                    return JsonResponse({"Status" : "rfid_not_found"})
                    
        return JsonResponse({"Status" : "VOCÊ NAO POSSUI ACESSO A ESTA PÁGINA"})
    return JsonResponse({"Status" : "VOCÊ NAO POSSUI ACESSO A ESTA PÁGINA"})

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
