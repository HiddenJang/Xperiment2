from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login', views.login_page, name='login_page'),
    path('registration', views.reg_page, name='reg_page'),
    path('', include('apps.scanner.urls')),
]