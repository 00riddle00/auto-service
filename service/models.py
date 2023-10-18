from django.db import models


class Car(models.Model):
    license_plate_no = models.CharField(
        verbose_name="License plate number", max_length=16
    )
    vin_code = models.CharField(
        verbose_name="VIN code", max_length=32, unique=True
    )
    car_model = models.ForeignKey(
        to="CarModel",
        verbose_name="Model",
        on_delete=models.SET_NULL,
        null=True,
    )
    client_name = models.CharField(verbose_name="Client's name", max_length=64)

    def __str__(self):
        return (
            f"{self.licence_plate_no} - {self.vin_code} ("
            f"{self.car_model}, {self.client_name})"
        )

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"


class CarModel(models.Model):
    make = models.CharField(verbose_name="Make", max_length=64)
    model = models.CharField(verbose_name="Model", max_length=64)
    year = models.IntegerField(verbose_name="Year")
    engine_type = models.CharField("Engine type", max_length=64)

    def __str__(self):
        return f"{self.make} {self.model}, {self.year}, {self.engine_type}"

    class Meta:
        verbose_name = "Car model"
        verbose_name_plural = "Car models"


class Service(models.Model):
    name = models.CharField(verbose_name="Name", max_length=128)
    price = models.FloatField(verbose_name="Price")

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
    total_price = models.FloatField(verbose_name="Total price")

    def __str__(self):
        return f"{self.date} ({self.car})"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


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
    price = models.IntegerField(null=False)
    quantity = models.IntegerField(verbose_name="Quantity")

    def __str__(self):
        return (
            f"{self.order} ({self.service}, {self.price} "
            f"€, qty: {self.quantity})"
        )

    class Meta:
        verbose_name = "Order line"
        verbose_name_plural = "Order lines"