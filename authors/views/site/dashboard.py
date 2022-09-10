from django.views.generic import TemplateView
from authors.views.site.dashboard_recipe_base import DashboardRecipeBase
from recipes.models import Recipe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class Dashboard(TemplateView, DashboardRecipeBase):
    template_name = 'authors/pages/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        recipes = self.get_recipes()
        ctx.update({'recipes': recipes})
        return ctx

