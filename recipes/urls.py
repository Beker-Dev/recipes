from django.urls import path
from . import views


app_name = 'recipes'
urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name='category'),
    path('recipes/<int:pk>/', views.RecipeListViewDetail.as_view(), name='detail'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/api/v1/', views.RecipeListViewHomeApiV1.as_view(), name='home_api_v1'),
    path('recipes/api/v1/<int:pk>/', views.RecipeListViewDetailApiV1.as_view(), name='detail_api_v1'),
]
