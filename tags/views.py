from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from tags.models import Tag
from tags.serializers import TagSerializer


class TagApiDetail(RetrieveAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
