from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class BuscarRfidForm(forms.Form):
    campo = forms.CharField(required=False, label="", max_length=50)

    def __init__(self, *args, **kwargs):
        super(BuscarRfidForm, self).__init__(*args, **kwargs)

        self.fields['campo'].widget.attrs = {
            'placeholder' : 'Insira a TagRfid',
        }

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'sr-only'
        self.helper.layout = Layout(
            'campo',

            Submit('submit', 'Buscar', css_id='botao_buscar', css_class='btn btn-primary mb-2')
        )