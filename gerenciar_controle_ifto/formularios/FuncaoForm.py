from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User
 
 
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