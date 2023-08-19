from . import views
from django.urls import path, include

urlpatterns = [
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register_user'),
    path('reset-password/', views.reset_password, name='reset_password'),
]