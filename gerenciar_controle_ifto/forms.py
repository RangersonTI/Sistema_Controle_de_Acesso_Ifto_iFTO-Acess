from django.forms.models import ModelForm
from django import forms
from django.db import models
from gerenciar_controle_ifto.models import *
 
class EditarTagRfid(forms.ModelForm):

    class Meta:
        model = Rfid
        fields = ["cod_corRFID_funcao", "data_desativacao", "ativo", "motivo_desativacao"]
        
    def __init__(self, *args, **kwargs):
        super(EditarTagRfid, self).__init__(*args, **kwargs)
        
        if "ativo" in kwargs['instance'] and kwargs['instance'].ativo:
            self.fields["data_desativacao"].required == False
            self.fields["motivo_desativacao"].required == False