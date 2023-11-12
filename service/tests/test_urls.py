from django.test import TestCase
from django.urls import resolve, reverse

from service.views import OrderDetailView, OrderListView, cars


class TestUrls(TestCase):
    def test_cars_url_is_resolved(self):
        url = reverse("cars")
        self.assertEqual(resolve(url).func, cars)

    def test_orders_url_is_resolved(self):
        url = reverse("orders")
        self.assertEqual(resolve(url).func.view_class, OrderListView)

    def test_order_details_url_is_resolved(self):
        url = reverse("order_details", args=[1])
        self.assertEqual(resolve(url).func.view_class, OrderDetailView)
