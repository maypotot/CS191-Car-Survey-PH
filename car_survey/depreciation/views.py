from django.shortcuts import render
from django.http import JsonResponse
from .models import Vehicle, Value
from .depreciation import predict_depreciation

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

    predicted_depreciation, predicted_depreciation_lst = predict_depreciation(maker, model, int(year))

    value = {'depreciation_value': predicted_depreciation, "highest_value": predicted_depreciation_lst.max(), "lowest_value": predicted_depreciation_lst.min()}
    return JsonResponse(value)

def data(request):
    context = {'vehicles': Vehicle.objects.all()}
    return render(request, 'fmv/data.html', context)
