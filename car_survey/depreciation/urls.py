from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='depreciation-home'),
    path('results/', views.results, name='depreciation-results'),
]
