from django.forms.models import ModelForm
from django import forms
from django.db import models
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
 

class EditarRfidForm(forms.Form):
    tag_rfid_value = forms.CharField(required=False, label="Tag Rfid",max_length=12, disabled=True)
    cod_corRFID_funcao = forms.ModelChoiceField(required=True, label="Cor Rfid:", queryset=CorRFID_Funcao.objects.all())
    ativo = forms.BooleanField(required=False, label="Ativo:")
    data_desativacao = forms.DateTimeField(required=False, label="Data de desativação:", 
                                           widget=forms.DateTimeInput(
                                               attrs={'type': 'datetime-local'},
                                               format='%Y-%m-%d %H:%M'),
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
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success')
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
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success')
        )
    
    def clean(self):
        cor_rfid_funcoes = CorRFID_Funcao.objects.all()
        corRfid = self.cleaned_data['corRFID']
                
        for cor_rfid_funcao in cor_rfid_funcoes:
            if str(corRfid).upper() == str(cor_rfid_funcao.corRFID).upper() and not(corRfid):
                self.add_error('corRFID', "A cor informada ja foi cadastrada")

        if len(corRfid) <=2:
            self.add_error('corRFID',"A cor deve ter mais de 2 caracteres")