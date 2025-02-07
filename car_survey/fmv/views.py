from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Vehicle
from .fmv import predict_fmv

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

    predicted_fmv, predicted_fmv_lst, = predict_fmv(maker, model, int(year))

    value = {'maker': maker, 'model': model,'value_price': predicted_fmv, "highest_value": predicted_fmv_lst.max(), "lowest_value": predicted_fmv_lst.min()}
    return JsonResponse(value)

def data(request):
    context = {'vehicles': Vehicle.objects.all()}
    return render(request, 'fmv/data.html', context)