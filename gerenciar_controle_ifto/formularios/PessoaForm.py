from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User
 

class EditarPessoaForm(forms.Form):
    id = forms.IntegerField()
    nome = forms.CharField(label="Nome:")
    sobrenome = forms.CharField(label="Sobrenome:")
    cpf = forms.CharField(label="CPF:")
    data_nascimento = forms.DateTimeField(label="Data de nascimento:",
                                          widget= forms.DateTimeInput(
                                                attrs={'type': 'date'},
                                                format='%d-%m-%Y'
                                            ),
                                        )
    cod_Papel_pessoa = forms.ModelChoiceField(label="Funcao",queryset=Papel_pessoa.objects.all())
    
    def __init__(self, *args, cod_cargoID=None, vinculado=False, id_pessoa=0, **kwargs):
        super(EditarPessoaForm,self).__init__(*args, **kwargs)
        
        self.fields['id'].initial = id_pessoa
        
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
        
        if vinculado == False:
            self.fields['cod_Papel_pessoa'].widget.attrs = {
                'id' : 'cod_Papel_pessoa'
            }
        else:
            self.fields['cod_Papel_pessoa'].widget.attrs = {
                'disabled' : True
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
        id_pessoa = int(self.cleaned_data['id'])
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
            cpf_pessoa = Pessoa.objects.filter(cpf=cpf).exclude(id=id_pessoa)
            if cpf_pessoa:
                self.add_error('cpf', "CPF informado já foi cadastrado no sistema")
            else:
                cpf_p1 = cpf[:3]
                cpf_p2 = cpf[3:6]
                cpf_p3 = cpf[6:9]
                cpf_p4 = cpf[9:]
                cpf_particionado = "{}.{}.{}-{}".format(cpf_p1,cpf_p2,cpf_p3,cpf_p4)

                if not(cpf_validate.validate(cpf_particionado)):
                    self.add_error('cpf', "CPF informado é invalido")

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