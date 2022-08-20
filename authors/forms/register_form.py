from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import is_strong_password


class RegisterForm(forms.ModelForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email)
        if exists:
            raise ValidationError(
                'Email já está sendo utilizado, por favor informe outro email',
                code='invalid'
            )
        else:
            return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            password_confirmation_error = "Senhas não conferem"
            raise ValidationError({
                'password': password_confirmation_error, 'confirm_password': password_confirmation_error
            })

    first_name = forms.CharField(
        error_messages={'required': 'Campo Nome não pode ficar vazio'},
        label='Nome',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nome'
            }
        )
    )

    last_name = forms.CharField(
        error_messages={'required': 'Campo Sobrenome não pode ficar vazio'},
        label='Sobrenome',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Sobrenome'
            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput({
            'placeholder': 'Usuário',
            'class': 'input text-input'
        }),
        error_messages={
            'required': 'Campo Usuário não pode ficar vazio',
            'max_length': 'Esse campo deve conter no máximo 150 caracteres',
            'min_length': 'Esse campo deve conter no mínimo 4 caracteres',
            'invalid': 'Esse campo não é válido'
        },
        label='Usuário',
        help_text=(
            'Deve conter no mínimo 4 caracteres e no máximo 150 caracteres. Sendo, letras, números e @/./+/-/_ '
            'apenas.'
        ),
        max_length=150,
        min_length=4
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'placeholder': 'email@example.com'
        }),
        error_messages={
            'required': 'Campo Email não pode ficar vazio'
        },
        label='Email',
        help_text='Email deve ser válido',
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha'
        }),
        error_messages={'required': 'Campo Senha não pode ficar vazio'},
        label='Senha',
        help_text='Deve conter pelo menos oito caracteres, sendo um maiúsculo, um minusculo e um número',
        validators=[is_strong_password]
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar Senha'
        }),
        # error_messages={'required': 'Senhas não conferem'},
        label='Confirmar Senha',
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
