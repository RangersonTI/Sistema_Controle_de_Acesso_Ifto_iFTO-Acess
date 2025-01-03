from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User


class CadastrarCorRfidForm(forms.Form):
    corRFID = forms.CharField(label="Cor:")
    cod_cargo = forms.ModelChoiceField(label="Cargo:", queryset=Papel_pessoa.objects.filter(vinculado_corRfid=False))

    def __init__(self, *args, cod_cargoID=None, **kwargs):
        super(CadastrarCorRfidForm, self).__init__(*args, **kwargs)

        self.fields['corRFID'].widget.attrs = {
            'id' : 'corRFID'
        }

        self.fields['cod_cargo'].widget.attrs = {
            'id' : 'cod_cargo'
        }
        
        self.helper = FormHelper(self)
        self.helper.form_class= 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.layout = Layout(
            'corRFID',
            'cod_cargo',
            HTML("""<a href="{% url "visualizar_corRfid" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        corRfid_funcoes = CorRFID_Funcao.objects.all()
        corRfid = self.cleaned_data['corRFID']

        if len(corRfid) <=2:
            self.add_error('corRFID',"A cor deve ter mais de 2 caracteres")

        for corRfid_obj in corRfid_funcoes:
            if str(corRfid).upper() == corRfid_obj.corRFID.upper():
                self.add_error('corRFID', "Esta funcão já foi cadastrada.")
                break

 

class EditarCorRfidForm(forms.Form):
    id = forms.IntegerField()
    corRFID = forms.CharField(label="Cor:")
    cod_cargo = forms.ModelChoiceField(label="Cargo:", queryset=Papel_pessoa.objects.all())

    def __init__(self, *args, cod_cargoID=None, **kwargs):
        super(EditarCorRfidForm, self).__init__(*args, **kwargs)

        self.fields['id'].widget.attrs = {
            'readonly' : True
        }
        
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
            'id',
            'corRFID',
            'cod_cargo',
            HTML("""<a href="{% url "visualizar_corRfid" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        id = self.cleaned_data['id']
        corRfid = self.cleaned_data['corRFID']
        corRfid_exist = CorRFID_Funcao.objects.filter(corRFID=corRfid).exclude(id=id)

        if len(corRfid) <=2:
            self.add_error('corRFID',"A cor deve ter mais de 2 caracteres")

        if corRfid_exist:
            self.add_error('corRFID', "Esta funcão já foi cadastrada.")

class BuscarCorRfidForm(forms.Form):
    campo = forms.CharField(required=False, label="", max_length=50)

    def __init__(self, *args, **kwargs):
        super(BuscarCorRfidForm, self).__init__(*args, **kwargs)

        self.fields['campo'].widget.attrs = {
            'placeholder' : 'Busque por Cor ou Função',
            'title' : 'Busque por Cor ou Função',
        }

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'form-group mb-2'
        self.helper.layout = Layout(
            'campo',
            Submit('submit', 'Buscar', css_id='botao_buscar', css_class='btn btn-primary mb-2')
        )