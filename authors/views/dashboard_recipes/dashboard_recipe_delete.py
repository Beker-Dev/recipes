from .dashboard_recipe_base import DashboardRecipeBase
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipeBase):
    def post(self, *args, **kwargs):
        recipe_id = self.request.POST.get('recipe_id')
        recipe = self.get_recipe(recipe_id)
        recipe.delete()
        messages.info(self.request, 'Receita deletada com sucesso!')
        return redirect('authors:dashboard')

