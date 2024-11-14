from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User
 

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