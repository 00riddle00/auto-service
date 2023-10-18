from django.contrib import admin

from .models import Car, CarModel, Order, OrderLine, Service


class CarAdmin(admin.ModelAdmin):
    list_display = ["license_plate_no", "vin_code", "car_model", "client_name"]
    list_filter = ["client_name", "car_model__make", "car_model__model"]
    search_fields = ["license_plate_no", "vin_code"]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ("date", "car", "total_price")
    list_editable = "total_price"
    inlines = ["OrderLineInline"]


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    readonly_fields = ["id"]
    can_delete = False
    extra = 0


admin.site.register(Car)
admin.site.register(CarModel)
admin.site.register(Service)
admin.site.register(Order)
admin.site.register(OrderLine)
