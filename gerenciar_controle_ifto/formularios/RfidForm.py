from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User


class CadastrarRfidForm(forms.Form):
    tag_rfid_value = forms.CharField(required=True, label="Tag Rfid",max_length=12)
    cod_corRFID_funcao = forms.ModelChoiceField(required=True, label="Cor Rfid:", queryset=CorRFID_Funcao.objects.all())
    ativo = forms.BooleanField(required=False, label="Ativo:", initial=True)
    data_desativacao = forms.DateTimeField(required=False, label="Data de desativação:", 
                                           widget=forms.DateTimeInput(
                                               attrs={'type': 'datetime-local'},
                                               format='%Y-%m-%d'),
                                           disabled=True,
                                           )
    motivo_desativacao = forms.CharField(required=False, label="Motivo desativação:",max_length=30, disabled=True)

    def __init__(self, *args, **kwargs):
        super(CadastrarRfidForm, self).__init__(*args, **kwargs)
        
        self.fields['tag_rfid_value'].widget.attrs = {
            'readonly':True
        }

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
                    </a>
                    <a href="">
                        <button type='button' class="btn btn-danger", onclick="leitura_rfid()" id="botao_ler_rfid">Ler RFID</button>
                    </a>
                    """),
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

class EditarRfidForm(forms.Form):
    tag_rfid_value = forms.CharField(label="Tag Rfid",max_length=12)
    cod_corRFID_funcao = forms.ModelChoiceField(required=True, label="Cor Rfid:", queryset=CorRFID_Funcao.objects.all())
    ativo = forms.BooleanField(required=False, label="Ativo:")
    data_desativacao = forms.DateTimeField(required=False, label="Data de desativação:", 
                                           widget=forms.DateTimeInput(
                                               attrs={'type': 'date'},
                                               format='%Y-%m-%d'),
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
        
        self.fields['tag_rfid_value'].widget.attrs = {
            'readonly' : True,
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

        print("\n")
        print(ativo)
        print(data_desativacao)
        print(motivo_desativacao)
        print("\n")
        
        if ativo == False and ((data_desativacao == None or data_desativacao == "") or (motivo_desativacao == None or motivo_desativacao == "")):
            self.add_error('data_desativacao',"")
            self.add_error('motivo_desativacao',"")
            raise ValidationError("Os campos 'Data de desativação' e 'Motivo desativação' são obrigatório quanto 'Ativo' for falso")