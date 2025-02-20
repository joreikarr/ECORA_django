from django.urls import path
from . import views
from .views import initiative_detail

urlpatterns = [
    path('', views.home, name='home'),
    path('initiatives/', views.initiatives, name='initiatives'),
    path('articles/', views.articles, name='articles'),
    path('change-language/', views.change_language, name='change_language'),
    path('contact/', views.contact, name='contact'),
    path('initiatives/<int:initiative_id>/', initiative_detail, name='initiative_detail'),
]
