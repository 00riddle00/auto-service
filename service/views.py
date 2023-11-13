import re

import pandas as pd
import plotly.express as px
import plotly.offline as po
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.translation import gettext as _
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin

from .forms import (
    OrderCommentForm,
    OrderForm,
    ProfileUpdateForm,
    UserUpdateForm,
)
from .models import Car, Order, OrderLine, Service


def index(request):
    num_cars = Car.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders = Order.objects.filter(status__exact="C").count()
    num_visits = request.session.get(key="num_visits", default=1)
    request.session["num_visits"] = num_visits + 1

    df = pd.DataFrame(
        {
            "item": [_("Cars"), _("Services"), _("Orders")],
            "count": [num_cars, num_services, num_orders],
        }
    )

    fig = px.bar(
        df,
        x="item",
        y="count",
        color_discrete_sequence=["#386b58"],
        title=_("Overview:"),
        labels={"item": _("item"), "count": _("count")},
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
    return render(request, template_name="cars.html", context={"cars": paged_cars})


def car(request, pk):
    car_ = get_object_or_404(Car, pk=pk)
    return render(request, template_name="car_details.html", context={"car": car_})


def search(request):
    query = request.GET.get("query")
    search_results = Car.objects.filter(
        Q(car_model__make__icontains=query) | Q(car_model__model__icontains=query)
    )
    return render(
        request,
        template_name="search_cars.html",
        context={"cars": search_results, "query": query},
    )


class ServiceListView(generic.ListView):
    model = Service
    paginate_by = 5
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


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    context_object_name = "order"
    form_class = OrderCommentForm
    template_name = "order_details.html"

    # Specify where to redirect after comment is successfully posted.
    def get_success_url(self):
        return reverse(viewname="order_details", kwargs={"pk": self.object.id})

    # Standard post method override using FormMixin, can be copied directly
    # to our project.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # Specify that the order will be the one after which we comment,
    # and the user will be the one who is logged in.
    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 5
    context_object_name = "user_orders"
    template_name = "user_orders.html"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("deadline")


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    success_url = "/my-orders/"
    form_class = OrderForm
    template_name = "order_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "order_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return reverse(viewname="order_details", kwargs={"pk": self.kwargs["pk"]})


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    success_url = "/my-orders/"
    context_object_name = "order"
    template_name = "order_delete.html"

    def test_func(self):
        return self.get_object().user == self.request.user


class OrderLineCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = OrderLine
    fields = ["service", "quantity"]
    template_name = "order_line_form.html"

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs["pk"])
        form.save()
        return super().form_valid(form)

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs["pk"])
        return order.user == self.request.user

    def get_success_url(self):
        return reverse(viewname="order_details", kwargs={"pk": self.kwargs["pk"]})


class OrderLineUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = OrderLine
    fields = ["service", "quantity"]
    template_name = "order_line_form.html"

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs["order_pk"])
        form.save()
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().order.user == self.request.user

    def get_success_url(self):
        return reverse(viewname="order_details", kwargs={"pk": self.kwargs["order_pk"]})


class OrderLineDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = OrderLine
    context_object_name = "order_line"
    template_name = "order_line_delete.html"

    def test_func(self):
        return self.get_object().order.user == self.request.user

    def get_success_url(self):
        return reverse(viewname="order_details", kwargs={"pk": self.kwargs["order_pk"]})


@csrf_protect
def register(request):
    if request.method == "POST":
        # Get values from registration form.
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        # Check if all fields are filled.
        if username == "" or email == "" or password == "":
            messages.error(request, message=_("Please fill in all fields!"))
            return redirect("register")
        # Check if passwords match.
        elif password != password2:
            messages.error(request, message=_("Passwords do not match!"))
            return redirect("register")
        # Check if password is strong enough.
        elif not re.match(
            string=password, pattern=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
        ):
            messages.error(
                request,
                message=_(
                    "Password must be minimum 8 characters long, contain at least one "
                    "letter and one number."
                ),
            )
            return redirect("register")
        # Check if username exists.
        elif User.objects.filter(username=username).exists():
            messages.error(
                request,
                message=_("User with username {username_bold} already exists!").format(
                    username_bold=f"<strong>{username}</strong>"
                ),
            )
            return redirect("register")
        # Check if there is already a user with this email.
        elif User.objects.filter(email=email).exists():
            messages.error(
                request,
                message=_("User with email {email_bold} already exists!").format(
                    email_bold=f"<strong>{email}</strong>"
                ),
            )
            return redirect("register")
        # If everything is ok, create new user.
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.info(
                request,
                message=_("User {username_bold} successfully registered!").format(
                    username_bold=f"<strong>{username}</strong>"
                ),
            )
            return redirect("register_complete")
    return render(request, template_name="registration/register.html")


def register_complete(request):
    return render(request, template_name="registration/register_complete.html")


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, message=_("Profile updated"))
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, template_name="profile.html", context=context)
