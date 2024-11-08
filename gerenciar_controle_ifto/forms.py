from django.forms.models import ModelForm
from django import forms
from django.db import models
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User
 

class EditarRfidForm(forms.Form):
    tag_rfid_value = forms.CharField(required=False, label="Tag Rfid",max_length=12, disabled=True)
    cod_corRFID_funcao = forms.ModelChoiceField(required=True, label="Cor Rfid:", queryset=CorRFID_Funcao.objects.all())
    ativo = forms.BooleanField(required=False, label="Ativo:")
    data_desativacao = forms.DateTimeField(required=False, label="Data de desativação:", 
                                           widget=forms.DateTimeInput(
                                               attrs={'type': 'datetime-local'},
                                               format='%Y-%m-%d %H:%M'),
                                           disabled=True,
                                           )
    motivo_desativacao = forms.CharField(required=False, label="Motivo desativação:",max_length=30, disabled=True)

    def __init__(self, *args, corRfidID=None, **kwargs):
        super(EditarRfidForm, self).__init__(*args, **kwargs)

        if corRfidID is not None:
            corRfid = CorRFID_Funcao.objects.filter(id=corRfidID)
            other_options = CorRFID_Funcao.objects.exclude(id=corRfidID)
            self.fields['cod_corRFID_funcao'].queryset = corRfid | other_options

        self.fields['ativo'].widget.attrs = {
            'id' : 'rfid_ativo',
        }

        self.fields['data_desativacao'].widget.attrs = {
            'id' : 'data_desativacao',
        }

        self.fields['motivo_desativacao'].widget.attrs = {
            'id' : 'motivo_desativacao',
        }

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'tag_rfid_value',
            'cod_corRFID_funcao',
            'ativo',
            'data_desativacao',
            'motivo_desativacao',
            HTML("""<a href="{% url "visualizar_tagRfid" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success')
        )

    def clean(self):
        ativo = self.cleaned_data['ativo']
        data_desativacao = self.cleaned_data['data_desativacao']
        motivo_desativacao = self.cleaned_data['motivo_desativacao']

        if ativo == False and ((data_desativacao == None or data_desativacao == "") or (motivo_desativacao == None or motivo_desativacao == "")):
            self.add_error('data_desativacao',"")
            self.add_error('motivo_desativacao',"")
            raise ValidationError("Os campos 'Data de desativação' e 'Motivo desativação' são obrigatório quanto 'Ativo' for falso")


class EditarFuncaoForm(forms.Form):
    funcao = forms.CharField(label="Funcao:", required=True)
    
    def __init__(self, *args, **kwargs):
        super(EditarFuncaoForm, self).__init__(*args, **kwargs)
        
        self.fields['funcao'].widget.attrs = {
            'id' : 'funcao_descricao',
        }
        
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'funcao',
            HTML("""<a href="{% url "visualizar_funcao" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        funcoes = Papel_pessoa.objects.all()
        funcao = self.cleaned_data['funcao']

        if len(funcao) <=2:
            return self.add_error('funcao',"A funcao devera ter mais de 2 caracteres")
        
        for funcao_obj in funcoes:
            if str(funcao).upper() == funcao_obj.descricao.upper():
                self.add_error('funcao', "Esta funcao j'a foi cadastrada.")
                break


class EditarCorRfidForm(forms.Form):
    corRFID = forms.CharField(label="Cor:")
    cod_cargo = forms.ModelChoiceField(label="Cargo:", queryset=Papel_pessoa.objects.all())

    def __init__(self, *args, cod_cargoID=None, **kwargs):
        super(EditarCorRfidForm, self).__init__(*args, **kwargs)

        self.fields['corRFID'].widget.attrs = {
            'id' : 'corRFID'
        }

        self.fields['cod_cargo'].widget.attrs = {
            'id' : 'cod_cargo'
        }

        if cod_cargoID is not None:
            cod_cargo =Papel_pessoa.objects.filter(id=cod_cargoID)
            others_options = Papel_pessoa.objects.exclude(id=cod_cargoID).filter(vinculado_corRfid=False)
            self.fields['cod_cargo'].queryset = cod_cargo | others_options

        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'corRFID',
            'cod_cargo',
            HTML("""<a href="{% url "visualizar_corRfid" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        cor_rfid_funcoes = CorRFID_Funcao.objects.all()
        corRfid = self.cleaned_data['corRFID']

        for cor_rfid_funcao in cor_rfid_funcoes:
            if str(corRfid).upper() == str(cor_rfid_funcao.corRFID).upper() and not(corRfid):
                self.add_error('corRFID', "A cor informada ja foi cadastrada")

        if len(corRfid) <=2:
            self.add_error('corRFID',"A cor deve ter mais de 2 caracteres")

class EditarPessoaForm(forms.Form):
    nome = forms.CharField(label="Nome:")
    sobrenome = forms.CharField(label="Sobrenome:")
    cpf = forms.CharField(label="CPF:")
    data_nascimento = forms.DateTimeField(label="Data de nascimento:", 
                                          widget= forms.DateTimeInput(
                                                attrs={'type': 'datetime-local'},
                                                format='%d-%m-%Y %H:%M'
                                            ),
                                        )
    cod_Papel_pessoa = forms.ModelChoiceField(label="Funcao",queryset=Papel_pessoa.objects.all())
    
    def __init__(self, *args, cod_cargoID=None, **kwargs):
        super(EditarPessoaForm,self).__init__(*args, **kwargs)
        
        self.fields['nome'].widget.attrs = {
            'id' : 'nome'
        }
        self.fields['sobrenome'].widget.attrs = {
            'id' : 'sobrenome'
        }
        self.fields['cpf'].widget.attrs = {
            'id' : 'cpf',
            'maxlength' : 11
        }
        self.fields['data_nascimento'].widget.attrs = {
            'id' : 'data_nascimento',
            'min' : '1900-01-01'
        }
        self.fields['cod_Papel_pessoa'].widget.attrs = {
            'id' : 'cod_Papel_pessoa'
        }
        
        if cod_cargoID is not None:
            cod_cargo =Papel_pessoa.objects.filter(id=cod_cargoID)
            others_options = Papel_pessoa.objects.exclude(id=cod_cargoID)
            self.fields['cod_Papel_pessoa'].queryset = cod_cargo | others_options
        
        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'nome',
            'sobrenome',
            'cpf',
            'data_nascimento',
            'cod_Papel_pessoa',
            
            HTML("""<a href="{% url "visualizar_pessoa" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        nome = self.cleaned_data['nome']
        sobrenome = self.cleaned_data['sobrenome']
        cpf = self.cleaned_data['cpf']
        cpf_validate = CPF()

        if len(nome) <=2:
            self.add_error('nome',"O nome devera ter pelo menos 3 caracteres")

        if len(sobrenome) <=2:
            self.add_error('nome',"O sobrenome devera ter pelo menos 3 caracteres")

        if len(cpf) != 11:
            self.add_error('cpf','CPF incompleto')
        else:
            cpf_pessoa = Pessoa.objects.filter(cpf=cpf)
            if cpf_pessoa:
                self.add_error('cpf', "CPF informado j'a foi cadastrado no sistema")
            else:
                cpf_p1 = cpf[:3]
                cpf_p2 = cpf[3:6]
                cpf_p3 = cpf[6:9]
                cpf_p4 = cpf[9:]
                cpf_particionado = "{}.{}.{}-{}".format(cpf_p1,cpf_p2,cpf_p3,cpf_p4)

                if not(cpf_validate.validate(cpf_particionado)):
                    self.add_error('cpf', "CPF informado e invalido")

class VincularPessoaRfid(forms.Form):
    pessoa= forms.CharField(label="Pessoa:", disabled=True, required=False)
    rfid_a_vincular = forms.ModelChoiceField(queryset=Rfid.objects.all(),label="RFID:")

    def __init__(self, *args, codCargoID = None ,**kwargs):
        super(VincularPessoaRfid, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'pessoa',
            'rfid_a_vincular',

            HTML("""<a href="{% url "visualizar_pessoa" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

        if codCargoID is not None:
            rfid = Rfid.objects.filter(cod_corRFID_funcao_id=CorRFID_Funcao.objects.get(cod_cargo_id=codCargoID), vinculado=False)
            self.fields['rfid_a_vincular'].queryset = rfid


    def clean(self):
        rfid_a_vincular = self.cleaned_data['rfid_a_vincular']

        if rfid_a_vincular == None:
            self.add_error('rfid_a_vincular',"Selecione um RFID para vincular")
            
            
# PARA USUARIOS (CADASTRAR, EDITAR E LISTAR)

class UsuarioForm(forms.Form):
    nome = forms.CharField(label="Nome:")   
    sobrenome = forms.CharField(label="Sobrenome:")
    #cod_pessoa = forms.ModelChoiceField(label="Pessoa", queryset=Pessoa.objects.all())
    email = forms.EmailField(label="Email:")
    usuario = forms.CharField(label="Usuario:")
    senha = forms.CharField(label="Senha:", 
                            widget=forms.PasswordInput(
                                render_value=False
                            ))
    ativo = forms.BooleanField(label="Ativo:")

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        
        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'nome',
            'sobrenome',
            'email',
            'usuario',
            'senha',
            'ativo',
            HTML("""<a href="{% url "visualizar_usuario" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )
        
    def clean(self):
        nome = self.cleaned_data['nome']
        sobrenome = self.cleaned_data['sobrenome']
        email = self.cleaned_data['email']
        usuario = self.cleaned_data['usuario']
        senha = self.cleaned_data['senha']
        
        email_exist = User.objects.filter(email=email).first()
        usuario_exist = User.objects.filter(username=usuario).first()

        if email_exist:
            self.add_error('email', "O email informado já foi cadastrado em outro usuario")
        
        if usuario_exist:
            self.add_error('usuario',"O usuario informado já foi cadastrado em outro usuario")
            
        if len(usuario) <5:
            self.add_error('usuario',"O nome de'usuario' deverá ter pelo menos 5 caracteres")

        if len(senha) <8:
            self.add_error('senha',"A 'senha' deverá ter pelo menos 8 caracteres")
        else:
            if usuario.upper() == senha.upper():
                self.add_error('senha',"A 'senha' não pode ser igual ao nome de usuário")