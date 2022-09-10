from .recipe_list_view_base import RecipeListViewBase


class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self):
        qs = super().get_queryset()
        tag_slug = self.kwargs.get('slug')
        qs = qs.filter(tags__slug=tag_slug)
        return qs
