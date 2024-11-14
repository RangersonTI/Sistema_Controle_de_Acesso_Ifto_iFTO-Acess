from django import forms
from gerenciar_controle_ifto.models import Papel_pessoa, Pessoa, Rfid, CorRFID_Funcao
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from validate_docbr import CPF
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    usuario = forms.CharField(label=False)
    senha = forms.CharField(label=False, widget=forms.PasswordInput(
                                render_value=False
                            ))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        
        self.fields['usuario'].widget.attrs = {
            'placeholder' : "Usuario"
        }
        
        self.fields['senha'].widget.attrs = {
            'placeholder' : "Senha"
        }
        
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            'usuario',
            'senha',
            Submit('submit', 'Entrar', css_id='botao_entrar', css_class='btn btn-lg btn-success btn-block'),
            HTML("""<p class="mt-5 mb-3 text-muted">&copy; {{ano_criado}}{% if ano_criado < ano_atual %}-{{ano_atual}}{% endif %}""")
        )
    
    def clean(self):
        usuario = self.cleaned_data['usuario']
        senha = self.cleaned_data['senha']
        
        try:
            user = User.objects.get(username=usuario.lower())
        except Exception:
            raise ValidationError("Usuário ou senha inválido")
            
        if not(usuario == user.username and user.check_password(senha)):
           raise ValidationError("Usuário ou senha inválido")