from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .dashboard_recipe_base import DashboardRecipeBase
from authors.forms.author_recipe_form import AuthorRecipeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'  # decorate method dispatch "from View class"
)
class DashboardRecipeCreate(DashboardRecipeBase):
    def render_dashboard_recipe_create(self, form: AuthorRecipeForm) -> HttpResponse:
        return render(self.request, 'authors/pages/dashboard_recipe_create.html', {'form': form})

    def get(self, *args, **kwargs) -> HttpResponse:
        form = self.get_form()
        return self.render_dashboard_recipe_create(form)

    def post(self, *args, **kwargs) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            self.save_form(form)
            messages.success(self.request, 'Receita criada com sucesso!')
            return redirect('authors:dashboard')
        else:
            return self.render_dashboard_recipe_create(form)
