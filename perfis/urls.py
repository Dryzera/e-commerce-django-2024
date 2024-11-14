from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'perfis'

urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('atualizar/', views.Atualizar.as_view(), name='atualizar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]