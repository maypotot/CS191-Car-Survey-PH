from csv import Error
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Vehicle, Value
from .depreciation import predict_depreciation
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Require token authentication
@permission_classes([IsAuthenticated])  # Require login
def secure_data(request):
    return Response({"message": "This is a protected API!"})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])  # Require token authentication
@permission_classes([IsAuthenticated])  # Require login
def home(request):
    maker = request.GET.get('maker', 'Unknown Maker')
    model = request.GET.get('model', 'Unknown Model')
    # transmission = request.GET.get('transmission', 'Any Transmission')
    year = request.GET.get('year', 'Unknown Year')
    mileage = request.GET.get('mileage', 'Unknown Odometer')
    # variant = request.GET.get('variant', 'Unknown Odometer')
    # fuel = request.GET.get('fuel', 'Unknown Odometer')
    # vehicle = request.GET.get('vehicle', 'Unknown Odometer')

    userinput = {"maker": maker, 
             "model": model, 
            #  "transmission": transmission,
             "year": year,
            #  "vehicle": vehicle,
            #  "variant": variant,
            #  "fuel": fuel,
             "mileage": mileage}
    if year == "":
        year = 0
    else:
        year = int(year)
    if mileage == "":
        mileage = 0
    else:
        mileage = int(mileage)
    try:
        predicted_depreciation, predicted_depreciation_lst = predict_depreciation(input_maker=maker, input_model=model, input_year=year, input_mileage=mileage)
    except Error:
        return HttpResponse("Invalid input. Please check your input and try again.")
    value = {'maker': maker, 'model': model,'value_price': predicted_depreciation, "list_values": predicted_depreciation_lst[:10]}
    return JsonResponse(value)

def data(request):
    context = {'vehicles': Vehicle.objects.all()}
    return render(request, 'fmv/data.html', context)
