from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter


app_name = 'authors'

author_api_router = SimpleRouter()
author_api_router.register('api', views.AuthorViewSet, basename='api')

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('dashboard/recipe/<int:recipe_id>/edit', views.DashboardRecipeEdit.as_view(), name='dashboard_recipe_edit'),
    path('dashboard/recipe/create/', views.DashboardRecipeCreate.as_view(), name='dashboard_recipe_create'),
    path('dashboard/recipe/delete/', views.DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete'),
    path('profile/<int:profile_id>/', views.ProfileView.as_view(), name='profile')
]
urlpatterns += author_api_router.urls
