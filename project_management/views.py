from django.http import HttpResponse
from django.shortcuts import render

from .models import Car, CarModel, Order, OrderLine, Service


# Create your views here.
def index(request):
    # Let's count some of the main objects
    num_cars = Car.objects.all().count()
    num_models = CarModel.objects.all().count()

    # Order lines which are priced below 100
    order_lines_below_100 = OrderLine.objects.filter(price__lt=100).count()

    # How many services
    num_services = Service.objects.all().count()

    # We transfer information to ta template through a dictionary "context"
    context = {
        "num_cars": num_cars,
        "num_models": num_models,
        "order_lines_below_100": order_lines_below_100,
        "num_services": num_services,
    }

    # Render index.html with our data in a variable named "context"
    return render(request, "index.html", context=context)
