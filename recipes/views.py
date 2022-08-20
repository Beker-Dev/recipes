from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from utils.pagination import make_pagination_range, make_pagination
from .models import Recipe, Category
import os


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def home(request: WSGIRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/home.html',
        context={'recipes': page_object, 'pagination_range': pagination_range},
        status=200
    )


def detail(request: WSGIRequest, pk: int) -> HttpResponse:
    recipe = get_object_or_404(Recipe, id=pk, is_published=True)
    return render(request, 'recipes/pages/detail.html', context={'recipe': recipe, 'is_detail_page': True})


def category(request: WSGIRequest, category_id: int) -> HttpResponse:
    recipes = get_list_or_404(
        Recipe.objects.filter(category__id=category_id, is_published=True).order_by('-id')
    )
    category_name = recipes[0].category
    page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(
        request,
        'recipes/pages/category.html',
        context={
            'recipes': page_object,
            'pagination_range': pagination_range,
            'category_name': category_name
        },
        status=200
    )


def search(request: WSGIRequest) -> HttpResponse:
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    else:
        recipes = Recipe.objects.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True
        ).order_by('-id')
        page_object, pagination_range = make_pagination(request, recipes, PER_PAGE)
        return render(request, 'recipes/pages/search.html', {
            'recipes': page_object,
            'pagination_range': pagination_range,
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}'
        })
