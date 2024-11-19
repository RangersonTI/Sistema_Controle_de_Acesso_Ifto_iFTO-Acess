from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML


class BuscarRfidForm(forms.Form):
    campo = forms.CharField(required=False, label="", max_length=50)
    busca_data = forms.BooleanField(required=False, label="Data?")
    def __init__(self, *args, **kwargs):
        super(BuscarRfidForm, self).__init__(*args, **kwargs)

        self.fields['campo'].widget.attrs = {
            'placeholder' : 'Informe um Nome ou SobreNome',
        }
        
        self.fields['busca_data'].widget.attrs = {
            'id' : 'buscar_por_data',
            'onclick' : 'BuscaFormatData()',
        }
        


        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'sr-only'
        self.helper.layout = Layout(
            #HTML("""
            #    <div onclick="BuscaFormatData()">
            #        <input type="checkbox" onclick="BuscaFormatData()" id='busca_data' name='busca_data'>
            #        <label for='busca_data' onclick="BuscaFormatData()">Data?</label>
            #    </div>
            #     """),
            'busca_data',
            'campo',

            Submit('submit', 'Buscar', css_id='botao_buscar', css_class='btn btn-primary mb-2')
        )