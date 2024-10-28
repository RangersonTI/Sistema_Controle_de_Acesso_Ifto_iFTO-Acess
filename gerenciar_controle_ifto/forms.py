from django.forms.models import ModelForm
from django import forms
from django.db import models
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
 
#class EditarRfid(forms.ModelForm):
#
#    class Meta:
#        model = Rfid
#        fields = ["cod_corRFID_funcao", "data_desativacao", "ativo", "motivo_desativacao"]
#        
#    #def __init__(self, *args, **kwargs):
#    #    super(EditarRfid, self).__init__(*args, **kwargs)
#    #    
#    #    if "ativo" in kwargs['instance'] and kwargs['instance'].ativo:
#    #        self.fields["data_desativacao"].required == False
#    #        self.fields["motivo_desativacao"].required == False

class EditarRfidForm(forms.Form):
    tag_rfid_value = forms.CharField(required=False, label="Tag Rfid",max_length=12, disabled=True)
    cod_corRFID_funcao = forms.ModelChoiceField(label="Cor Rfid:", queryset=CorRFID_Funcao.objects.all(), empty_label="Selecione uma opcao")
    ativo = forms.BooleanField(label="Ativo:", initial=True)
    data_desativacao = forms.DateTimeField(required=False, label="Data de desativação:", 
                                           widget=forms.DateTimeInput(
                                               attrs={'type': 'datetime-local'},
                                               format='%Y-%m-%d %H:%M')
                                           )
    motivo_desativacao = forms.CharField(required=False, label="Motivo desativação:",max_length=30)
    
    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)
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
        )

    def clean(self):
        ativo = self.cleaned_data['ativo']
        data_desativacao = self.cleaned_data['data_desativacao']
        motivo_desativacao = self.cleaned_data['motivo_desativacao']
        
        if ativo == True and (data_desativacao == None and motivo_desativacao == None):
            raise ValidationError("Os campos 'Data de desatvação' e 'Motivo desativação' são obrigatório qual ativo seja 'Falso'")
