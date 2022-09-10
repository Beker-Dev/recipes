from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from .recipe_pagination_v1 import RecipePaginationV1
from recipes.permissions import IsOwner
from django.shortcuts import get_object_or_404

from django.urls import reverse


class RecipeViewSetV1(ModelViewSet):
    queryset = Recipe.objects.get_all_published_and_author_full_name()
    serializer_class = RecipeSerializer
    pagination_class = RecipePaginationV1
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']

    def filter_by_category(self, qs):
        category_name = self.request.query_params.get('category')
        if category_name:
            qs = qs.filter(category__name__iexact=category_name)
        return qs

    def filter_by_author(self, qs):
        author_name = self.request.query_params.get('author')
        if author_name:
            qs = qs.filter(author__username__iexact=author_name)
        return qs

    def apply_filters(self, qs):
        filters = (self.filter_by_category, self.filter_by_author)
        for filter in filters:
            qs = filter(qs)
        return qs

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.get_queryset(), pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner()]
        else:
            return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.kwargs:
            qs = self.apply_filters(qs)
        return qs

    def create(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

