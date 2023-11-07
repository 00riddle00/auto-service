from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from tinymce.models import HTMLField

utc = pytz.utc


class Car(models.Model):
    license_plate_no = models.CharField(
        verbose_name=_("License plate number"),
        max_length=16,
        help_text=_(
            "Enter car's licence plate number (it need not be unique, "
            "since cars can be from different countries)"
        ),
    )
    vin_code = models.CharField(
        verbose_name=_("VIN code"),
        max_length=17,
        unique=True,
        help_text=_("Enter car's VIN code (it must be unique)"),
    )

    car_model = models.ForeignKey(
        to="CarModel",
        verbose_name=_("Model"),
        on_delete=models.SET_NULL,
        null=True,
    )
    client_name = models.CharField(
        verbose_name=_("Client's name"), max_length=64
    )
    observations = models.TextField(
        verbose_name=_("Observations"), max_length=2048, default=""
    )
    photo = models.ImageField(
        verbose_name=_("Photo"),
        upload_to="car_photos",
        default="car_photos/no_photo.jpg",
    )

    def __str__(self):
        return (
            f"{self.license_plate_no} - {self.vin_code} ("
            f"{self.car_model}, {self.client_name})"
        )

    class Meta:
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 1000 or img.width > 1000:
            output_size = (1000, 1000)
            img.thumbnail(output_size)
            img.save(self.photo.path)


class CarModel(models.Model):
    make = models.CharField(verbose_name=_("Make"), max_length=64)
    model = models.CharField(verbose_name=_("Model"), max_length=64)
    year = models.IntegerField(verbose_name=_("Year"))
    engine_type = models.CharField(
        verbose_name=_("Engine type"), max_length=64
    )
    fuel_type = models.CharField(verbose_name=_("Fuel type"), max_length=64)
    description = HTMLField(
        verbose_name=_("Description"), max_length=4096, default=""
    )

    def __str__(self):
        return (
            f"{self.make} {self.model}, {self.year}, {self.engine_type}, "
            f"{self.fuel_type}"
        )

    class Meta:
        verbose_name = _("Car model")
        verbose_name_plural = _("Car models")


class Service(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    price = models.FloatField(verbose_name=_("Price"))
    description = HTMLField(
        verbose_name=_("Description"), max_length=4096, default=""
    )

    def __str__(self):
        return f"{self.name} ({self.price} €)"

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class Order(models.Model):
    date = models.DateField(verbose_name=_("Date"), auto_now_add=True)
    car = models.ForeignKey(
        to="Car",
        verbose_name=_("Car"),
        on_delete=models.CASCADE,
        related_name="orders",
    )

    ORDER_STATUS = (
        ("N", _("New")),
        ("D", _("Declined")),
        ("A", _("Accepted")),
        ("P", _("In Progress")),
        ("C", _("Completed")),
    )

    status = models.CharField(
        verbose_name=_("Status"),
        max_length=1,
        choices=ORDER_STATUS,
        default="N",
        blank=True,
    )

    deadline = models.DateTimeField(
        verbose_name=_("Deadline"), null=True, blank=True
    )

    user = models.ForeignKey(
        to=User,
        verbose_name=_("User"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.date} ({self.car})"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
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
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name="lines",
    )
    service = models.ForeignKey(
        to="Service",
        verbose_name=_("Service"),
        on_delete=models.SET_NULL,
        null=True,
    )
    quantity = models.IntegerField(verbose_name=_("Quantity"), default=1)

    @property
    def price(self):
        return self.service.price * self.quantity

    def __str__(self):
        qty = _("qty")
        return (
            f"{self.order}, {self.price} € ({self.service}, "
            f"{qty}: {self.quantity})"
        )

    class Meta:
        verbose_name = _("Order line")
        verbose_name_plural = _("Order lines")


class OrderComment(models.Model):
    order = models.ForeignKey(
        to="Order",
        verbose_name=_("Order"),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        to=User, verbose_name=_("Author"), on_delete=models.CASCADE
    )
    date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    text = models.TextField(verbose_name=_("Text"), max_length=2048)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-date"]


class Profile(models.Model):
    user = models.OneToOneField(
        to=User, verbose_name=_("User"), on_delete=models.CASCADE
    )
    picture = models.ImageField(
        verbose_name=_("Picture"),
        upload_to="profile_pics",
        default="profile_pics/default.png",
    )

    def __str__(self):
        profile = _("profile")
        return f"{self.user.username} {profile}"

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.picture.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.picture.path)
