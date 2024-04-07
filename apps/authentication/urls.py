from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login', views.login_page, name='login_page'),
    path('registration', views.reg_page, name='reg_page'),
]