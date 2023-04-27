from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CalcForm, OrderForm
from .models import (
    Insurance, 
    ShippingRates, 
    Client, 
    CityDeliveryRates, 
    DeliveryTime, 
    )


def select_factor(weight: float, volume: float) -> float:
    # Определяем коэффициент масса/объем
    if weight > volume * 250:   
        factor = weight
    else:
        factor = volume * 250
    return factor

def select_tariff(factor: float) -> str:
    # Определяем тариф, в зависимости от коэффициента масса/объем
    if 50 >= factor:
        name_column = 'rateUnder50'
    elif 50 > factor >= 100:
        name_column = 'rateUnder100'
    elif 100 > factor >= 200:
        name_column = 'rateUnder200'
    elif 200 > factor >= 300:
        name_column = 'rateUnder300'
    elif 300 > factor >= 500:
        name_column = 'rateUnder400'
    elif 500 > factor >= 1000:
        name_column = 'rateUnder100'
    else:
        name_column = 'rateOver1000'
    return name_column

def local_delivery_calculator(city, weight: float, volume: float) -> float:
    # Расчет доставки по городу
    factor = select_factor(weight, volume)
    name_column = select_tariff(factor)
    local_delivery_priсe = getattr(
        CityDeliveryRates.objects.get(city=city), 
        name_column
        ) * factor
    return local_delivery_priсe
    
def base_delivery_calculator(from_city, to_city, weight: float, volume: float) -> float: 
    #Расчет доставки между городами.
    factor = select_factor(weight, volume)
    name_column = select_tariff(factor)
    base_priсe = getattr(
        ShippingRates.objects.get(
        fromTheCity=from_city, 
        toTheCity=to_city,
        ), 
        name_column) * factor
    return base_priсe

def get_insurance(insurance_sum: int) -> float:
    # Расчет страховки
    insurance = Insurance.objects.all().first()   
    if insurance.rate * insurance_sum > insurance.priceMin:
        insurance_price = insurance.rate * insurance_sum
    else: 
        insurance_price = insurance.priceMin
    return insurance_price


def discount_get(request) -> int:
    # Расчет скидки
    if request.user.is_authenticated:
        discount = Client.objects.get(clientUser=request.user).discount
    else:
        discount = 0 
    return discount

def get_delivery_time(from_city, to_city) -> int:
    return DeliveryTime.objects.filter(fromTheCity=from_city, toTheCity=to_city).first().deliveryTime


def calculator_order(instance):
    # Калькулятор для заказа
    base_priсe = int(base_delivery_calculator(instance.fromCity, instance.toCity, instance.weight, instance.volume))
    insurance_price = int(get_insurance(instance.insurance_sum))
    if instance.deliveryFronCity == 'WD': 
        price_from_city = int(local_delivery_calculator(instance.fromCity, instance.weight, instance.volume))
    else:
        price_from_city = 0
    if instance.deliveryToCity == 'WD':
        price_to_city = int(local_delivery_calculator(instance.toCity, instance.weight, instance.volume))
    else:
        price_to_city = 0
    total_price = int((base_priсe + insurance_price) * (1 - instance.discount / 100) + price_from_city + price_to_city)

    return total_price


def calculator(request):
    # Калькулятор основной
    if request.method == 'GET':
        form = CalcForm(request.GET)
        if form.is_valid():
            from_city = form.cleaned_data['from_city']
            to_city = form.cleaned_data['to_city']
            delivery_from_city = form.cleaned_data['delivery_from_city']
            delivery_to_city = form.cleaned_data['delivery_to_city']
            weight = form.cleaned_data['weight']
            volume = form.cleaned_data['volume']
            insurance = form.cleaned_data['insurance']
            if from_city == to_city:
                delivery_time = 0
                base_priсe = 0
            else:
                delivery_time = get_delivery_time(from_city, to_city)   # срок доставки 
                base_priсe = int(base_delivery_calculator(from_city, to_city, weight, volume))   # цена доставки между городами
            insurance_price = int(get_insurance(insurance))   # цена страховки
            discount = int(discount_get(request))   # скидка
            if delivery_from_city == 'WD': 
                price_from_city = int(local_delivery_calculator(from_city, weight, volume))
            else:
                price_from_city = 0
            if delivery_to_city == 'WD':
                price_to_city = int(local_delivery_calculator(to_city, weight, volume))
            else:
                price_to_city = 0
            total_price = int((base_priсe + insurance_price + price_from_city + price_to_city) * (1 - discount / 100))
            result = {
                'from_city': from_city, 
                'to_city': to_city, 
                'insurance_price': insurance_price, 
                'base_priсe': base_priсe, 
                'discount': discount, 
                'total_price': total_price, 
                'delivery_time': delivery_time,
                'price_from_city': price_from_city,
                'price_to_city': price_to_city,
                'insurance': insurance,
                'delivery_from_city': delivery_from_city,
                'delivery_to_city': delivery_to_city,
                'weight': weight,
                'volume': volume,
                }
        else:
            form = CalcForm()
            result = False
        return (result, form)


