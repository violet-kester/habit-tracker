from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('add-habit/', views.add_habit, name='add_habit'),
    path('toggle-habit/', views.toggle_habit, name='toggle_habit'),
]
