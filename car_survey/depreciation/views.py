from django.shortcuts import render
from .models import UserInput


def home(request):
    context = {'vehicles': UserInput.objects.all()}
    return render(request, 'depreciation/home.html', context)


def results(request):
    return render(request, 'depreciation/results.html', {'title': 'Results'})
