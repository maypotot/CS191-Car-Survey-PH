from csv import Error
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Vehicle, Value
from .depreciation import predict_depreciation

def home(request):
    maker = request.GET.get('maker', 'Unknown Maker')
    model = request.GET.get('model', 'Unknown Model')
    transmission = request.GET.get('transmission', 'Any Transmission')
    year = request.GET.get('year', 'Unknown Year')
    odometer = request.GET.get('odometer', 'Unknown Odometer')
    vehicle = request.GET.get('vehicle', 'Unknown Odometer')

    userinput = {"maker": maker,
                 "model": model,
                 "transmission": transmission,
                 "year": year,
                 "vehicle": vehicle,
                 "odometer": odometer}
    try:
        predicted_depreciation, predicted_depreciation_lst = predict_depreciation(maker, model, int(year), vehicle)
    except Error:
        return HttpResponse("Invalid input. Please check your input and try again.")
    value = {'depreciation_value': predicted_depreciation, "values": predicted_depreciation_lst}
    return JsonResponse(value)

def data(request):
    context = {'vehicles': Vehicle.objects.all()}
    return render(request, 'fmv/data.html', context)
