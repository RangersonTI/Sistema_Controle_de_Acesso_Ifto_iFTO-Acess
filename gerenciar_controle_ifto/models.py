from django.db import models

# Create your models here.

class Papel_pessoa(models.Model):
    descricao = models.CharField(max_length=25)
    vinculado_corRfid = models.BooleanField()
    
    def __str__(self):
        return self.descricao

class CorRFID_Funcao(models.Model):
    corRFID = models.CharField(max_length=12, unique=True)
    cod_cargo = models.OneToOneField(Papel_pessoa, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.corRFID


class Rfid(models.Model):
    tag_rfid_value = models.CharField(max_length=12, unique=True)
    cod_corRFID_funcao = models.ForeignKey(CorRFID_Funcao, on_delete=models.PROTECT)
    data_cadastro = models.DateTimeField(editable=False)
    data_desativacao = models.DateTimeField(null=True)
    vinculado = models.BooleanField(null=True)
    ativo = models.BooleanField()
    motivo_desativacao = models.CharField(max_length=30, null=True)
    
    def data_formatada(self):
        if(self.data_desativacao):
            return self.data_desativacao.strftime("%d/%m/%Y, %H:%M")
        
class Pessoa(models.Model):
    nome = models.CharField(max_length=20)
    sobrenome = models.CharField(max_length=35)
    cpf = models.CharField(max_length=14, unique=True)
    data_nascimento = models.DateField()
    idade = models.IntegerField()
    cod_Papel_pessoa = models.ForeignKey(Papel_pessoa, on_delete=models.PROTECT)
    cod_Rfid = models.OneToOneField(Rfid, on_delete=models.PROTECT, null=True)
    vinculado = models.BooleanField()

class Usuario_sistema(models.Model):
    cod_pessoa = models.OneToOneField(Pessoa, on_delete=models.PROTECT)
    nome_de_usuario = models.CharField(max_length=20)
    usuario = models.CharField(max_length=15)
    senha = models.CharField(max_length=30)
    data_criacao = models.DateTimeField(auto_now_add=True,editable=False)
    
class Historico_acesso_campus(models.Model):
    cod_rfid = models.ForeignKey(Rfid, on_delete=models.PROTECT)
    cod_pessoa = models.ForeignKey(Pessoa, on_delete=models.PROTECT)
    funcao_pessoa = models.ForeignKey(Papel_pessoa, on_delete=models.PROTECT)
    data_acesso = models.DateTimeField(auto_now_add=True)