from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML


class BuscarHistoricoAcessoForm(forms.Form):
    campo = forms.CharField(required=False, label="", max_length=50)
    busca_data = forms.BooleanField(required=False, label="Data?")
    def __init__(self, *args, **kwargs):
        super(BuscarHistoricoAcessoForm, self).__init__(*args, **kwargs)

        self.fields['campo'].widget.attrs = {
            'placeholder' : 'Busque por Data, Nome ou Sobrenome',
            'title' : 'Busque por Data, Nome ou Sobrenome',
        }
        
        self.fields['busca_data'].widget.attrs = {
            'id' : 'buscar_por_data',
            'onclick' : 'BuscaFormatData()',
        }


        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'form-group mb-2'
        self.helper.layout = Layout(
            'busca_data',
            'campo',
            Submit('submit', 'Buscar', css_id='botao_buscar', css_class='btn btn-primary mb-2')
        )