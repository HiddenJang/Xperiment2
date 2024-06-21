from django.urls import path
from . import views

urlpatterns = [
    path('scanner', views.scan_page, name='scan_page'),
    #path('api/v1/start/', views.run_scanning),
    path('api/v1/start/', views.ScannerStarter.as_view()),
]