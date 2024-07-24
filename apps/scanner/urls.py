from django.urls import path
from . import views

urlpatterns = [
    path('scanner', views.scan_page, name='scan_page'),
    path('api/v2/start/', views.TestStarter.as_view()),
    path('api/v1/start/', views.ScannerStarter.as_view()),
]