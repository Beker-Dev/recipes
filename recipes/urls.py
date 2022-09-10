from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
from recipes.models import Recipe
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'recipes'

recipe_api_v2_router = SimpleRouter()
recipe_api_v2_router.register('recipes/api/v1', views.RecipeViewSetV1, basename='api-v1')

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/category/<int:category_id>/', views.RecipeListViewCategory.as_view(), name='category'),
    path('recipes/<int:pk>/', views.RecipeListViewDetail.as_view(), name='detail'),
    path('recipes/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipes/tag/<slug:slug>/', views.RecipeListViewTag.as_view(), name='tag'),
    path('recipes/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('recipes/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('recipes/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(recipe_api_v2_router.urls))
]
