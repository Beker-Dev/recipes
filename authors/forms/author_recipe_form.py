from django import forms
from recipes.models import Recipe
from django.core.exceptions import ValidationError


class AuthorRecipeForm(forms.ModelForm):
    cover = forms.ImageField(
        label='Imagem',
        widget=forms.FileInput(
            attrs={
                'class': 'span-2',
            }
        )
    )

    preparation_steps = forms.CharField(
        label='Passos de preparação',
        widget=forms.Textarea(
            attrs={
                'class': 'span-2',
                'placeholder': 'Passos de preparação'
            }
        )
    )

    servings_unit = forms.CharField(
        widget=forms.Select(
            choices=(
                ('Portions', 'Porções'),
                ('Pieces', 'Pedaços'),
                ('Slices', 'Fatias'),
            )
        )
    )

    preparation_time_unit = forms.CharField(
        widget=forms.Select(
            choices=(
                ('Minutes', 'Minutos'),
                ('Hours', 'Horas'),
            )
        )
    )

    def clean_title(self):
        title = self.cleaned_data.get('title')
        required_length = 4
        if len(title) < required_length:
            raise ValidationError(
                f'Titulo deve conter pelo menos {required_length} caracteres',
                code='invalid'
            )
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        required_length = 8
        if len(description) < required_length:
            raise ValidationError(
                f'Descrição deve conter pelo menos {required_length} caracteres',
                code='invalid'
            )
        return description

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')
        if not preparation_time > 0:
            raise ValidationError(
                'Valor invalido',
                code='invalid'
            )
        return preparation_time

    def clean_preparation_time_unit(self):
        preparation_time_unit = self.cleaned_data.get('preparation_time_unit')
        valid_time_unit = ('Minutes', 'Hours')
        if preparation_time_unit not in valid_time_unit:
            raise ValidationError(
                'Valor invalido',
                code='invalid'
            )
        return preparation_time_unit

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if not servings > 0:
            raise ValidationError(
                'Valor invalido',
                code='invalid'
            )
        return servings

    def clean_servings_unit(self):
        servings_unit = self.cleaned_data.get('servings_unit')
        valid_servings_unit = ('Portions', 'Pieces', 'Slices')
        if servings_unit not in valid_servings_unit:
            raise ValidationError(
                'Valor invalido',
                code='invalid'
            )
        return servings_unit

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category is None:
            raise ValidationError(
                'Selecione uma categoria',
                code='required'
            )
        return category

    def clean_preparation_steps(self):
        preparation_steps = self.cleaned_data.get('preparation_steps')
        required_length = 10
        if not len(preparation_steps) > required_length:
            raise ValidationError(
                f'Passos de preparação deve conter pelo menos {required_length} caracteres',
                code='invalid'
            )
        return preparation_steps

    class Meta:
        model = Recipe
        fields = (
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'category',
            'preparation_steps',
            'cover'
        )
