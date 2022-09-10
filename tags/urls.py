from django.urls import path
from . import views


app_name = 'tags'
urlpatterns = [
    path('api/v1/detail/<int:pk>/', views.TagApiDetail.as_view(), name='api-v1-detail')
]
