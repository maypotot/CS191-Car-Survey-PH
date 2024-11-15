from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'fmv-home'),
    path('data/', views.data, name='fmv-data'),
    path('results/', views.results, name='fmv-results'),
]