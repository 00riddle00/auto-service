import pandas as pd
import plotly.express as px
import plotly.offline as po
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Car, Order, Service


def index(request):
    num_cars = Car.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders = Order.objects.filter(status__exact="C").count()
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

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
        "num_visits": num_visits,
    }

    return render(request, "index.html", context=context)


def cars(request):
    paginator = Paginator(Car.objects.all(), per_page=5)
    page_number = request.GET.get("page")
    paged_cars = paginator.get_page(page_number)
    return render(request, "cars.html", context={"cars": paged_cars})


def car(request, pk):
    car_ = get_object_or_404(Car, pk=pk)
    return render(request, "car_details.html", context={"car": car_})


def search(request):
    query = request.GET.get("query")
    search_results = Car.objects.filter(
        Q(car_model__make__icontains=query)
        | Q(car_model__model__icontains=query)
    )
    return render(
        request,
        "search_cars.html",
        context={"cars": search_results, "query": query},
    )


class ServiceListView(generic.ListView):
    model = Service
    context_object_name = "services"
    template_name = "services.html"


class ServiceDetailView(generic.DetailView):
    model = Service
    context_object_name = "service"
    template_name = "service_details.html"


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 5
    context_object_name = "orders"
    template_name = "orders.html"


class OrderDetailView(generic.DetailView):
    model = Order
    context_object_name = "order"
    template_name = "order_details.html"


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 5
    context_object_name = "user_orders"
    template_name = "user_orders.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by(
            "deadline"
        )
