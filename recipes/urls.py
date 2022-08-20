from django.urls import path
from . import views


app_name = 'recipes'
urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/category/<int:category_id>/', views.category, name='category'),
    path('recipes/<int:pk>/', views.detail, name='detail'),
    path('recipes/search/', views.search, name='search'),
]
