from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest
from authors.forms.author_recipe_form import AuthorRecipeForm
from django.urls import reverse
from .dashboard_recipe_base import DashboardRecipeBase
from recipes.models import Recipe
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'  # decorate method dispatch "from View class"
)
class DashboardRecipeEdit(DashboardRecipeBase):
    def render_dashboard_recipe_edit(self, recipe: Recipe, form: AuthorRecipeForm) -> HttpResponse:
        return render(self.request, 'authors/pages/dashboard_recipe_edit.html', {'recipe': recipe, 'form': form})

    def get(self, *args, **kwargs) -> HttpResponse:
        recipe_id = kwargs.get('recipe_id')
        recipe = self.get_recipe(recipe_id)
        form = self.get_form(recipe)
        return self.render_dashboard_recipe_edit(recipe, form)

    def post(self, *args, **kwargs) -> HttpResponse:
        recipe_id = kwargs.get('recipe_id')
        recipe = self.get_recipe(recipe_id)
        form = self.get_form(recipe)
        if form.is_valid():
            self.save_form(form)
            messages.success(self.request, 'Receita salva com sucesso!')
            return redirect(reverse('authors:dashboard_recipe_edit', kwargs={'recipe_id': recipe.id}))
        else:
            return self.render_dashboard_recipe_edit(recipe, form)
