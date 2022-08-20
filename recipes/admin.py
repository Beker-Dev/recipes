from django.contrib import admin
from .models import Recipe, Category


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'is_published', 'preparation_steps_is_html', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'author__username', 'category__name', 'description', 'slug', 'preparation_steps')
    list_editable = ('is_published', 'preparation_steps_is_html')
    list_filter = ('is_published', 'category', 'preparation_steps_is_html')
    list_per_page = 10
    ordering = ('-id',)
    prepopulated_fields = {
        'slug': ('title',)
    }


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
