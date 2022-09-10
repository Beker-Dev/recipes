from .recipe_list_view_base import RecipeListViewBase


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        qs = qs.filter(category__id=category_id)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        category_name = context['recipes'][0].category.name if context['recipes'] else ''
        page_title = 'Category'
        context.update({
            'page_title': page_title + ' | ' + category_name
        })
        return context

