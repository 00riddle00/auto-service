from django.test import TestCase
from django.urls import reverse

from service.models import Service


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
