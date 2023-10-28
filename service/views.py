import pandas as pd
import plotly.express as px
import plotly.offline as po
from django.contrib import messages
from django.contrib.auth.forms import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.views.decorators.csrf import csrf_protect

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

    return render(request, template_name="index.html", context=context)


def cars(request):
    paginator = Paginator(Car.objects.all(), per_page=5)
    page_number = request.GET.get("page")
    paged_cars = paginator.get_page(page_number)
    return render(
        request, template_name="cars.html", context={"cars": paged_cars}
    )


def car(request, pk):
    car_ = get_object_or_404(Car, pk=pk)
    return render(
        request, template_name="car_details.html", context={"car": car_}
    )


def search(request):
    query = request.GET.get("query")
    search_results = Car.objects.filter(
        Q(car_model__make__icontains=query)
        | Q(car_model__model__icontains=query)
    )
    return render(
        request,
        template_name="search_cars.html",
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


@csrf_protect
def register(request):
    if request.method == "POST":
        # Get values from registration form.
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        # Check if passwords match.
        if password == password2:
            # Check if username exists.
            if User.objects.filter(username=username).exists():
                messages.error(
                    request,
                    message=f"User <strong>{username}</strong> already "
                    f"exists!",
                )
                return redirect("register")
            else:
                # Check if there is already a user with this email.
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request,
                        message=f"User with email <strong>{email}</strong> "
                        f"already exists!",
                    )
                    return redirect("register")
                else:
                    # If everything is ok, create new user.
                    User.objects.create_user(
                        username=username, email=email, password=password
                    )
                    messages.info(
                        request,
                        message=f"User <strong>{username}</strong> "
                        f"successfully registered!",
                    )
                    return redirect("login")
        else:
            messages.error(request, message="Passwords do not match!")
            return redirect("register")
    return render(request, template_name="registration/register.html")
