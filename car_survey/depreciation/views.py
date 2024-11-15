from django.shortcuts import render
from django.http import JsonResponse
from .models import Vehicle, Value

def home(request):
    maker = request.GET.get('maker', 'Unknown Maker')
    model = request.GET.get('model', 'Unknown Model')
    transmission = request.GET.get('transmission', 'Any Transmission')
    year = request.GET.get('year', 'Unknown Year')
    odometer = request.GET.get('odometer', 'Unknown Odometer')
    price = request.GET.get('price', 'Unknown Price')

    userinput = {"maker": maker,
                 "model": model,
                 "transmission": transmission,
                 "year": year,
                 "odometer": odometer,
                 "price": price}

    return JsonResponse(userinput)

def results(request):
    value = {'depreciation': ""}
    return JsonResponse(value)
