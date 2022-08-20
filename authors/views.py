from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib import messages
from .forms.register_form import RegisterForm
from .forms.login_form import LoginForm
from .forms.author_recipe_form import AuthorRecipeForm
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe


def register_view(request: WSGIRequest) -> HttpResponse:
    register_form_data = request.session.get('register_form_data')
    form = RegisterForm(register_form_data)
    form_action = reverse('authors:register_create')
    return render(request, 'authors/pages/register.html', {'form': form, 'form_action': form_action})


def register_create(request: WSGIRequest) -> HttpResponse:
    if not request.POST:
        raise Http404()
    else:
        post = request.POST
        request.session['register_form_data'] = post
        form = RegisterForm(post)

        if form.is_valid():
            author = form.save(commit=False)
            author.set_password(author.password)
            author.save()
            messages.success(request, 'Usuário registrado com sucesso!')
            del request.session['register_form_data']
            return redirect('authors:login')
        else:
            messages.error(request, 'Há erros no formulário, verifique e envie novamente!')
            return redirect('authors:register')


def login_view(request: WSGIRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('authors:dashboard')
    else:
        form = LoginForm()
        form_action = reverse('authors:login_create')
        return render(request, 'authors/pages/login.html', {'form': form, 'form_action': form_action})


def login_create(request: WSGIRequest) -> HttpResponse:
    if not request.POST:
        raise Http404()
    else:
        post = request.POST
        form = LoginForm(post)
        if form.is_valid():
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            authenticated_user = authenticate(username=username, password=password)

            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('authors:dashboard')

        messages.error(request, 'Usuário ou Senha invalidos')
        return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request: WSGIRequest) -> HttpResponse:
    if not request.POST:
        raise Http404()
    else:
        username_logged_in = request.user.username
        username_in_form = request.POST.get('username')

        if username_logged_in != username_in_form:
            return HttpResponseForbidden()
        else:
            logout(request)
            return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request: WSGIRequest) -> HttpResponse:
    author = request.user
    recipes = Recipe.objects.filter(author=author, is_published=False)
    return render(request, 'authors/pages/dashboard.html', {'recipes': recipes})


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request: WSGIRequest, recipe_id: int) -> HttpResponse:
    author = request.user
    recipe = get_object_or_404(Recipe, author=author, is_published=False, id=recipe_id)
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.save()
        messages.success(request, 'Receita salva com sucesso!')
        return redirect(reverse('authors:dashboard_recipe_edit', kwargs={'recipe_id': recipe.id}))

    return render(request, 'authors/pages/dashboard_recipe_edit.html', {'recipe': recipe, 'form': form})


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request: WSGIRequest) -> HttpResponse:
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.save()
        messages.success(request, 'Receita criada com sucesso!')
        return redirect('authors:dashboard')
    else:
        return render(request, 'authors/pages/dashboard_recipe_create.html', {'form': form})


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request: WSGIRequest) -> HttpResponse:
    if not request.POST:
        return HttpResponseForbidden()
    else:
        recipe_id = request.POST.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe.delete()
        messages.info(request, 'Receita deletada com sucesso!')
        return redirect('authors:dashboard')
