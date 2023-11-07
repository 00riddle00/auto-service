import datetime

from django.test import TestCase
from PIL import Image

from service.models import Car, CarModel, Order


class TestCar(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_vin_length(self):
        """Test that the max length of VIN code is 17."""
        car = Car.objects.get(id=1)
        max_length = car._meta.get_field("vin_code").max_length
        self.assertEqual(max_length, 17)

    def test_car_photo_filename(self):
        """Test that the photo field is set to default photo for a new car."""
        car = Car.objects.get(id=1)
        self.assertEqual(car.photo.name, "car_photos/no_photo.jpg")

    def test_car_photo_size(self):
        """Test that the car photo size is not bigger than 1000px."""
        car = Car.objects.get(id=1)
        file = car.photo.file
        image = Image.open(file)
        image_shape = image.height, image.width
        self.assertFalse(any([size > 1000 for size in image_shape]))


class TestOrder(TestCase):
    @classmethod
    def setUpTestData(cls):
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
            deadline=datetime.date.today() - datetime.timedelta(days=1),
        )

    def test_overdue(self):
        """Test that the is_overdue property method works correctly."""
        order = Order.objects.get(id=1)
        self.assertTrue(order.is_overdue)

    def test_default_status(self):
        """Test that the default order status is set to 'New'."""
        order = Order.objects.all()[0]
        self.assertEqual(order.status, "N")
        self.assertEqual(order.get_status_display(), "New")
