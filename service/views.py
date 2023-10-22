import pandas as pd
import plotly.express as px
import plotly.offline as po
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Car, Order, Service


def index(request):
    num_cars = Car.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders = Order.objects.filter(status__exact="C").count()

    df = pd.DataFrame(
        {
            "items": ["Cars", "Services", "Orders"],
            "count": [num_cars, num_services, num_orders],
        }
    )

    fig = px.bar(
        df,
        x="items",
        y="count",
        color_discrete_sequence=["#386b58"],
        title="Overview:",
    )
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    fig.update_yaxes(dtick=1, ticks="outside", tickwidth=2, tickformat=",d")
    bar_chart = po.plot(fig, output_type="div")

    context = {
        "num_cars": num_cars,
        "num_services": num_services,
        "num_orders": num_orders,
        "bar_chart": bar_chart,
    }

    return render(request, "index.html", context=context)


def about(request):
    return render(request, "about.html")


def cars(request):
    cars_ = Car.objects.all()
    return render(request, "cars.html", {"cars": cars_})


def car(request, pk):
    car_ = get_object_or_404(Car, pk=pk)
    return render(request, "car_details.html", {"car": car_})


class ServiceListView(generic.ListView):
    model = Service
    context_object_name = "services"
    template_name = "services.html"


class ServiceDetailView(generic.DetailView):
    model = Service
    template_name = "service_details.html"


class OrderListView(generic.ListView):
    model = Order
    context_object_name = "orders"
    template_name = "orders.html"


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order_details.html"
