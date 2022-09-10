from rest_framework.generics import RetrieveAPIView
from tags.models import Tag
from tags.serializers import TagSerializer


class TagApiDetail(RetrieveAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
