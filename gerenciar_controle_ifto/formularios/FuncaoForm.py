from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User
 
class CadastrarFuncaoForm(forms.Form):
    funcao = forms.CharField(label="Funcao:", required=True)

    def __init__(self, *args, **kwargs):
        super(CadastrarFuncaoForm, self).__init__(*args, **kwargs)

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
            return self.add_error('funcao',"A funcão devera ter mais de 2 caracteres")
        
        for funcao_obj in funcoes:
            if str(funcao).upper() == funcao_obj.descricao.upper():
                self.add_error('funcao', "Esta funcão já foi cadastrada.")
                break
 
 
class EditarFuncaoForm(forms.Form):
    id = forms.IntegerField()
    funcao = forms.CharField(label="Funcao:", required=True)

    def __init__(self, *args, **kwargs):
        super(EditarFuncaoForm, self).__init__(*args, **kwargs)

        self.fields['id'].widget.attrs = {
            'readonly' : True
        }
        
        self.fields['funcao'].widget.attrs = {
            'id' : 'funcao_descricao',
        }

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'id',
            'funcao',
            HTML("""<a href="{% url "visualizar_funcao" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success'),
        )

    def clean(self):
        id=self.cleaned_data['id']
        funcao = self.cleaned_data['funcao']
        funcoao_exist = Papel_pessoa.objects.filter(descricao=funcao).exclude(id=id)

        if len(funcao) <=2:
            return self.add_error('funcao',"A funcao deverá ter mais de 2 caracteres")
        
        if funcoao_exist:
            self.add_error('funcao', "Esta funcao já foi cadastrada.")
            
class BuscarFuncaoForm(forms.Form):
    campo = forms.CharField(required=False, label="", max_length=50)

    def __init__(self, *args, **kwargs):
        super(BuscarFuncaoForm, self).__init__(*args, **kwargs)

        self.fields['campo'].widget.attrs = {
            'placeholder' : 'Informe a função',
        }

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'sr-only'
        self.helper.layout = Layout(
            'campo',

            Submit('submit', 'Buscar', css_id='botao_buscar', css_class='btn btn-primary mb-2')
        )