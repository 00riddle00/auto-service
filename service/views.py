from django.shortcuts import render

from .models import Car, CarModel, Order, Service


def index(request):
    num_cars = Car.objects.all().count()
    num_models = CarModel.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders = Order.objects.all().count()

    context = {
        "num_cars": num_cars,
        "num_models": num_models,
        "num_services": num_services,
        "num_orders": num_orders,
    }

    return render(request, "index.html", context=context)
