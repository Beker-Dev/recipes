from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from tag.models import Tag
from tag.serializers import TagSerializer


@api_view()
def tag_api_detail(request, pk: int):
    tag = get_object_or_404(Tag, pk=pk)
    serializer = TagSerializer(instance=tag)
    return Response(serializer.data)

