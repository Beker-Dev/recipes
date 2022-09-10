from django.views.generic import ListView
from recipes.models import Recipe
import os
from django.utils import translation


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = PER_PAGE
    ordering = ('-id',)
    template_name = None

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)
        qs = qs.select_related('author', 'category', 'author__profile')
        qs = qs.prefetch_related('tags')
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['html_language'] = translation.get_language()
        return context

