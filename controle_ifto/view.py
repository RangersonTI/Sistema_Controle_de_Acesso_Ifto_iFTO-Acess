import mysql.connector as mysql
import json

def validarAcesso(value_rfid):
    cursor,conexao_mysql = conexao()


def cadHistoricoAceso(request):
    return

def cadPessoa(nome_pessoa,rfid):
    
    cursor,conexao_mysql = conexao()
    
    command_sql = "INSERT INTO Pessoa(nome, cod_rfid) VALUE(%s,%s)"
    val = (nome_pessoa,rfid,)

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


nome_rfids = [{'nome' : "Sandra Costa", 'rfid' : 2}, 
         {'nome' : "Luis Felipe", 'rfid' : 4},
]

for nome_rfid in nome_rfids:
    cadPessoa(nome_rfid['nome'],nome_rfid['rfid'])

#rfids = ["W2 F4 5A QQ", "14 K8 80 00", "12 76 9A SX", "1C 5A 66 7Y", "2W 9U 7A PL", "Z3 R1 DA WY", "2E 4V VF YI"]
#
#for rfid in rfids:
#    cadRFID(rfid)

#papel_pessoa = ["Aluno", "Professor", "Tecnico Administrativo", "Visitante"]
#
#for papel in papel_pessoa:
#    cadPapelPessoa(papel)