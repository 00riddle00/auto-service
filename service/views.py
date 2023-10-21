from django.shortcuts import render

from .models import Car, Order, Service


def index(request):
    num_cars = Car.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders = Order.objects.filter(status__exact="C").count()

    context = {
        "num_cars": num_cars,
        "num_services": num_services,
        "num_orders": num_orders,
    }

    return render(request, "index.html", context=context)
