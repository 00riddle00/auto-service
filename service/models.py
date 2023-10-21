from django.db import models


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
    description = models.TextField("Description", max_length=2048, default="")

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

    def __str__(self):
        return f"{self.date} ({self.car})"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-id"]


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
