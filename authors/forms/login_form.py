from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuário'
            }
        )
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha'
            }
        )
    )
