from django.views import View
from recipes.models import Recipe
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from authors.forms.author_recipe_form import AuthorRecipeForm
from django.urls import reverse


class DashboardRecipeBase(View):
    def get_recipe(self, recipe_id: int) -> Recipe:
        recipe = get_object_or_404(Recipe, author=self.request.user, is_published=False, id=recipe_id)
        return recipe

    def get_form(self, recipe: Recipe = None) -> AuthorRecipeForm:
        form = AuthorRecipeForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=recipe
        )
        return form

    def save_form(self, form: AuthorRecipeForm) -> Recipe:
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        recipe.preparation_steps_is_html = False
        recipe.save()
        return recipe
