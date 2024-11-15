from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Vehicle
from .fmv import get_fmv

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

    fmv_dict, fmv = get_fmv(int(year), int(odometer), 5)

    value = {'value_price': fmv, "highest_value": fmv_dict[int(year) + 1], "lowest_value": fmv_dict[int(year) - 1]}
    return JsonResponse(value)

def data(request):
    context = {'vehicles': Vehicle.objects.all()}
    return render(request, 'fmv/data.html', context)