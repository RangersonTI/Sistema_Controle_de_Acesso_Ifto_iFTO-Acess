from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User


class CadastrarRfidForm(forms.Form):
    tag_rfid_value = forms.CharField(required=True, label="Tag Rfid",max_length=12)
    cod_corRFID_funcao = forms.ModelChoiceField(required=True, label="Cor Rfid:", queryset=CorRFID_Funcao.objects.all())
    ativo = forms.BooleanField(required=False, label="Ativo:", initial=True)
    data_desativacao = forms.DateTimeField(required=False, label="Data de desativação:", 
                                           widget=forms.DateTimeInput(
                                               attrs={'type': 'datetime-local'},
                                               format='%Y-%m-%d'),
                                           disabled=True,
                                           )
    motivo_desativacao = forms.CharField(required=False, label="Motivo desativação:",max_length=30, disabled=True)

    def __init__(self, *args, **kwargs):
        super(CadastrarRfidForm, self).__init__(*args, **kwargs)
        
        self.fields['tag_rfid_value'].widget.attrs = {
            'id' : 'tag_rfid_value',
            'readonly':True
        }

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
            HTML("""<a href="{% url "visualizar_tagRfid" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>
                    <button type='button' class="btn btn-danger", onclick="leitura_rfid()", id="botao_ler_rfid">Ler RFID</button>
                    """),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success')
        )

    def clean(self):
        tag_rfid_exist=None
        tag_rfid_value = self.cleaned_data['tag_rfid_value']
        ativo = self.cleaned_data['ativo']
        data_desativacao = self.cleaned_data['data_desativacao']
        motivo_desativacao = self.cleaned_data['motivo_desativacao']
        
        try:
            tag_rfid_exist = Rfid.objects.get(tag_rfid_value=tag_rfid_value)
        except:
            pass

        if tag_rfid_exist:
            self.add_error('tag_rfid_value',"Esta Tag-Rfid já foi cadastrada")
        
        if tag_rfid_value == "Nenhum card" or tag_rfid_value == "undefined":
            self.add_error('tag_rfid_value',"O leitor não identificou a informação da Tag. Favor, tentar novamente.")
        
        if ativo == False and ((data_desativacao == None or data_desativacao == "") or (motivo_desativacao == None or motivo_desativacao == "")):
            self.add_error('data_desativacao',"")
            self.add_error('motivo_desativacao',"")
            raise ValidationError("Os campos 'Data de desativação' e 'Motivo desativação' são obrigatório quanto 'Ativo' for falso")

class EditarRfidForm(forms.Form):
    tag_rfid_value = forms.CharField(label="Tag Rfid",max_length=12)
    cod_corRFID_funcao = forms.ModelChoiceField(required=True, label="Cor Rfid:", queryset=CorRFID_Funcao.objects.all())
    ativo = forms.BooleanField(required=False, label="Ativo:")
    data_desativacao = forms.DateTimeField(required=False, label="Data de desativação:", 
                                           widget=forms.DateTimeInput(
                                               attrs={'type': 'datetime-local'},
                                               format='%d-%m-%Y %H%M'),
                                           )
    motivo_desativacao = forms.CharField(required=False, label="Motivo desativação:",max_length=30)

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
            'disabled' : True
        }

        self.fields['motivo_desativacao'].widget.attrs = {
            'id' : 'motivo_desativacao',
            'disabled' : True
        }

        self.fields['tag_rfid_value'].widget.attrs = {
            'readonly' : True,
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
            HTML("""<a href="{% url "visualizar_tagRfid" %}">
                        <button type='button' class="btn btn-primary", id="botao_voltar">Voltar</button>
                    </a>"""),
            Submit('submit', 'Salvar', css_id='botao_salvar', css_class='btn btn-success')
        )

    def clean(self):
        ativo = self.cleaned_data['ativo']
        if not(ativo):
        
            data_desativacao = self.cleaned_data['data_desativacao']
            motivo_desativacao = self.cleaned_data['motivo_desativacao']

            print("\n")
            print(ativo)
            print(data_desativacao)
            print(motivo_desativacao)
            print("\n")
            
            if ((data_desativacao == None or data_desativacao == "") or (motivo_desativacao == None or motivo_desativacao == "")):
                self.add_error('data_desativacao',"")
                self.add_error('motivo_desativacao',"")
                raise ValidationError("Os campos 'Data de desativação' e 'Motivo desativação' são obrigatório quando 'Ativo' for falso")

class BuscarRfidForm(forms.Form):
    campo = forms.CharField(required=False, label="", max_length=50)

    def __init__(self, *args, **kwargs):
        super(BuscarRfidForm, self).__init__(*args, **kwargs)

        self.fields['campo'].widget.attrs = {
            'id' : 'campo',
            'placeholder' : 'Busque por TagRfid, Ativo(%at)/N.Ativo(%nat) ou Disponível(%disp)/N.Disponível(%ndisp)',
            'title' : 'Busque por TagRfid, Ativo(%at)/N.Ativo(%nat) ou Disponível(%disp)/ N.Disponível(%ndisp)',
        }

        self.helper = FormHelper(self)
        self.helper.form_class = 'form-inline'
        self.helper.label_class = 'sr-only'
        self.helper.field_class = 'form-group mb-2'
        self.helper.layout = Layout(
            'campo',
            Submit('submit', 'Buscar', css_id='botao_buscar', css_class='btn btn-primary mb-2'),
            HTML(""" <button type='button' class="btn btn-danger mb-2", onclick="leitura_rfid_listagem()", id="botao_ler_rfid_buscar">Ler RFID</button> """)
        )