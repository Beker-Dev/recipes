from django.views.generic import DetailView
from recipes.models import Recipe


class RecipeListViewDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(is_published=True)
        qs = qs.select_related('author', 'category')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'is_detail_page': True})
        return context
