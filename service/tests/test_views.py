import datetime

import pytz
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from service.models import Car, CarModel, Order, Service

utc = pytz.utc


class TestServiceListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        for service_id in range(1, 11):
            Service.objects.create(
                name="Tire mounting and wheel balancing", price=45
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/services/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("services"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("services"))
        self.assertTemplateUsed(response, template_name="services.html")

    def test_pagination_is_five(self):
        response = self.client.get(reverse("services"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["services"]), 5)


class TestUserOrderListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            username="john_doe", password="VerySecretPassword123"
        )

        CarModel.objects.create(
            make="Ford",
            model="Mondeo",
            year=2009,
            engine_type="2000 cm³, 107kW",
            fuel_type="Gasoline",
        )

        Car.objects.create(
            license_plate_no="FMC516",
            vin_code="WAUNE78P28A492843",
            car_model=CarModel.objects.get(id=1),
            client_name="John Doe",
        )

        Order.objects.create(
            car=Car.objects.get(id=1),
            user=test_user,
            deadline=datetime.datetime.today().replace(tzinfo=utc)
            + datetime.timedelta(days=3),
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(
            username="john_doe", password="VerySecretPassword123"
        )
        response = self.client.get(reverse("user-orders"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context["user"]), "john_doe")
        self.assertTemplateUsed(response, template_name="user_orders.html")

    def test_user_order_in_list(self):
        self.client.login(
            username="john_doe", password="VerySecretPassword123"
        )
        response = self.client.get(reverse("user-orders"))
        self.assertEqual(str(response.context["user"]), "john_doe")
        self.assertTrue("user_orders" in response.context)
        self.assertEqual(len(response.context["user_orders"]), 1)
        self.assertEqual(
            response.context["user_orders"][0].car.license_plate_no, "FMC516"
        )
