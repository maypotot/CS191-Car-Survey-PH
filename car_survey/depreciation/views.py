from django.shortcuts import render
from django.http import JsonResponse
from .models import Vehicle, Value


def home(request):
    context = {'vehicles': Vehicle.objects.all()}
    return render(request, 'depreciation/home.html', context)


def results(request):
    value = {'value_price': "", "highest_value": "", "lowest_value": ""}
    return JsonResponse(value)
