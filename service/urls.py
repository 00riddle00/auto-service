"""
URL configuration for service app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cars/", views.cars, name="cars"),
    path("cars/<int:pk>", views.car, name="car-details"),
    path("search-cars/", views.search, name="search-cars"),
    path("services", views.ServiceListView.as_view(), name="services"),
    path(
        "services/<int:pk>",
        views.ServiceDetailView.as_view(),
        name="service-details",
    ),
    path("orders/", views.OrderListView.as_view(), name="orders"),
    path(
        "orders/<int:pk>",
        views.OrderDetailView.as_view(),
        name="order-details",
    ),
    path(
        "my-orders/",
        views.UserOrderListView.as_view(),
        name="user-orders",
    ),
    path(
        "orders/new/",
        views.OrderCreateView.as_view(),
        name="order-new",
    ),
    path(
        "orders/<int:pk>/update/",
        views.OrderUpdateView.as_view(),
        name="order-update",
    ),
    path(
        "orders/<int:pk>/delete/",
        views.OrderDeleteView.as_view(),
        name="order-delete",
    ),
    path(
        "orders/<int:pk>/lines/new/",
        views.OrderLineCreateView.as_view(),
        name="order-line-new",
    ),
    path("profile/", views.profile, name="profile"),
]
