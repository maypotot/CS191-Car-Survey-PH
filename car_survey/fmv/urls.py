from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'fmv-home'),
    path('results/', views.results, name='fmv-results'),
]