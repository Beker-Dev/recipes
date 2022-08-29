from .recipe_list_view_base import RecipeListViewBase
from django.db.models import Q


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'
    paginate_by = 3

    def get_search_term(self):
        return self.request.GET.get('q', '').strip()

    def get_queryset(self):
        qs = super().get_queryset()
        search_term = self.get_search_term()
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_term = self.get_search_term()
        context.update({
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}'
        })
        return context
