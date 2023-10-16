from django.db import models


class CarModel(models.Model):
    make = models.CharField(max_length=20, unique=True, null=False)
    model = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return f"{self.make} {self.model}"


class Car(models.Model):
    plate_number = models.CharField(max_length=10, unique=True, null=False)
    car_model = models.ForeignKey(CarModel, null=False, on_delete=models.PROTECT)
    vin_code = models.CharField(max_length=100, unique=True, null=False)
    client = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.plate_number}"


class Service(models.Model):
    name = models.CharField(max_length=30, null=False)
    price = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    date = models.DateField(null=False)
    car = models.ForeignKey(Car, null=False, on_delete=models.PROTECT)
    sum = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.date}"


class OrderLine(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=False)
    price = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.quantity}"
