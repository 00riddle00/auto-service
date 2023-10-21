from django.shortcuts import get_object_or_404, render
from django.views import generic

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


def cars(request):
    cars_ = Car.objects.all()
    return render(request, "cars.html", {"cars": cars_})


def car(request, car_id):
    car_ = get_object_or_404(Car, pk=car_id)
    return render(request, "car_details.html", {"car": car_})


class ServiceListView(generic.ListView):
    model = Service
    template_name = "service_list.html"
