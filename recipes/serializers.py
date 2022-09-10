from rest_framework import serializers
from .models import Category, Recipe
from django.contrib.auth.models import User
from tag.models import Tag
from tag.serializers import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'description', 'author', 'category', 'public', 'preparation', 'tags', 'tag_links',
                  'preparation_time', 'servings', 'cover')

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(method_name='join_preparation', read_only=True)
    preparation_time = serializers.IntegerField(write_only=True)
    category = serializers.StringRelatedField()
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='recipes:api_v2_tag',
        read_only=True
    )

    def join_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, value):
        required_length = 4
        if len(value) < required_length:
            raise serializers.ValidationError(f'Titulo deve conter pelo menos {required_length} caracteres')
        return value

    def validate_description(self, value):
        required_length = 8
        if len(value) < required_length:
            raise serializers.ValidationError(f'Descrição deve conter pelo menos {required_length} caracteres')
        return value

    def validate_preparation_time(self, value):
        if not value > 0:
            raise serializers.ValidationError('Valor invalido')
        return value

    def validate_preparation_time_unit(self, value):
        valid_time_unit = ('Minutes', 'Hours')
        if value not in valid_time_unit:
            raise serializers.ValidationError('Valor invalido')
        return value

    def validate_servings(self, value):
        if not value > 0:
            raise serializers.ValidationError('Valor invalido')
        return value

    def validate_servings_unit(self, value):
        valid_servings_unit = ('Portions', 'Pieces', 'Slices')
        if value not in valid_servings_unit:
            raise serializers.ValidationError('Valor invalido')
        return value

    def validate_category(self, value):
        if value is None:
            raise serializers.ValidationError('Selecione uma categoria')
        return value

    def validate_preparation_steps(self, value):
        required_length = 10
        if not len(value) > required_length:
            raise serializers.ValidationError(f'Passos de preparação deve conter pelo menos {required_length} caracteres',)
        return value

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
