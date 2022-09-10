from django.db.models.aggregates import Count
from django.shortcuts import render

from recipes.models import Recipe


def theory(request):
    recipes = Recipe.objects.get_all_published_and_author_full_name()[:10]
    total_of_recipes = recipes.aggregate(Count('id')).get('id__count')
    context = {
        'recipes': recipes,
        'total_of_recipes': total_of_recipes
    }
    return render(request, 'recipes/pages/theory.html', context=context)
