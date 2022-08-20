from django.core.exceptions import ValidationError
import re


def is_strong_password(password: str):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError(
            'Deve conter pelo menos oito caracteres, sendo um maiúsculo, um minusculo e um número'
        )
