from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from tinymce.models import HTMLField

utc = pytz.utc


class Car(models.Model):
    license_plate_no = models.CharField(
        verbose_name="License plate number",
        max_length=16,
        help_text="Enter car's licence plate number (it need not be unique, "
        "since cars can be from different countries)",
    )
    vin_code = models.CharField(
        verbose_name="VIN code",
        max_length=32,
        unique=True,
        help_text="Enter car's vin code (it must be unique)",
    )

    car_model = models.ForeignKey(
        to="CarModel",
        verbose_name="Model",
        on_delete=models.SET_NULL,
        null=True,
    )
    client_name = models.CharField(verbose_name="Client's name", max_length=64)
    observations = models.TextField(
        verbose_name="Observations", max_length=2048, default=""
    )
    photo = models.ImageField(
        verbose_name="Photo", upload_to="car_photos", null=True, blank=True
    )

    def __str__(self):
        return (
            f"{self.license_plate_no} - {self.vin_code} ("
            f"{self.car_model}, {self.client_name})"
        )

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"


class CarModel(models.Model):
    make = models.CharField(verbose_name="Make", max_length=64)
    model = models.CharField(verbose_name="Model", max_length=64)
    year = models.IntegerField(verbose_name="Year")
    engine_type = models.CharField(verbose_name="Engine type", max_length=64)
    fuel_type = models.CharField(verbose_name="Fuel type", max_length=64)
    description = HTMLField(
        verbose_name="Description", max_length=4096, default=""
    )

    def __str__(self):
        return (
            f"{self.make} {self.model}, {self.year}, {self.engine_type}, "
            f"{self.fuel_type}"
        )

    class Meta:
        verbose_name = "Car model"
        verbose_name_plural = "Car models"


class Service(models.Model):
    name = models.CharField(verbose_name="Name", max_length=128)
    price = models.FloatField(verbose_name="Price")
    description = HTMLField(
        verbose_name="Description", max_length=4096, default=""
    )

    def __str__(self):
        return f"{self.name} ({self.price} €)"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class Order(models.Model):
    date = models.DateField(verbose_name="Date", auto_now_add=True)
    car = models.ForeignKey(
        to="Car",
        verbose_name="Car",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    ORDER_STATUS = (
        ("N", "New"),
        ("D", "Declined"),
        ("A", "Accepted"),
        ("P", "In Progress"),
        ("C", "Completed"),
    )

    status = models.CharField(
        verbose_name="Status",
        max_length=1,
        choices=ORDER_STATUS,
        default="N",
        blank=True,
    )

    deadline = models.DateTimeField(
        verbose_name="Deadline", null=True, blank=True
    )

    user = models.ForeignKey(
        to=User,
        verbose_name="User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.date} ({self.car})"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-id"]

    @property
    def total_price(self):
        total_price = 0
        for line in self.lines.all():
            total_price += line.price
        return total_price

    @property
    def is_overdue(self):
        return self.deadline and self.deadline.replace(
            tzinfo=utc
        ) < datetime.today().replace(tzinfo=utc)


class OrderLine(models.Model):
    order = models.ForeignKey(
        to="Order",
        verbose_name="Order",
        on_delete=models.CASCADE,
        related_name="lines",
    )
    service = models.ForeignKey(
        to="Service",
        verbose_name="Service",
        on_delete=models.SET_NULL,
        null=True,
    )
    quantity = models.IntegerField(verbose_name="Quantity", default=1)

    @property
    def price(self):
        return self.service.price * self.quantity

    def __str__(self):
        return (
            f"{self.order}, {self.price} € ({self.service}, "
            f"qty: {self.quantity})"
        )

    class Meta:
        verbose_name = "Order line"
        verbose_name_plural = "Order lines"


class OrderComment(models.Model):
    order = models.ForeignKey(
        to="Order",
        verbose_name="Order",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        to=User, verbose_name="Author", on_delete=models.CASCADE
    )
    date = models.DateTimeField(verbose_name="Date", auto_now_add=True)
    text = models.TextField(verbose_name="Text", max_length=2048)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-date"]


class Profile(models.Model):
    user = models.OneToOneField(
        to=User, verbose_name="User", on_delete=models.CASCADE
    )
    picture = models.ImageField(
        verbose_name="Picture",
        upload_to="profile_pics",
        default="profile_pics/default.png",
    )

    def __str__(self):
        return f"{self.user.username} profile"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
