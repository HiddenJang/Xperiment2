from django.urls import path
from . import views

urlpatterns = [
    path('scanner/', views.scanner_page, name='scanner_page'),
]