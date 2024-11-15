from django.shortcuts import render
from django.http import JsonResponse
from .models import Vehicle, Value

def home(request):
    maker = request.GET.get('maker', 'Unknown Maker')
    model = request.GET.get('model', 'Unknown Model')
    transmission = request.GET.get('transmission', 'Any Transmission')
    year = request.GET.get('year', 'Unknown Year')
    odometer = request.GET.get('odometer', 'Unknown Odometer')

    userinput = {"maker": maker,
                 "model": model,
                 "transmission": transmission,
                 "year": year,
                 "odometer": odometer}

    value = {'depreciation': ""}
    return JsonResponse(value)
