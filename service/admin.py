from django.contrib import admin

from .models import Car, CarModel, Order, OrderLine, Service


class CarAdmin(admin.ModelAdmin):
    list_display = [
        "license_plate_no",
        "vin_code",
        "car_model",
        "client_name",
        "observations",
    ]
    list_filter = ["client_name", "car_model__make", "car_model__model"]
    search_fields = ["license_plate_no", "vin_code"]


class CarModelAdmin(admin.ModelAdmin):
    list_display = [
        "make",
        "model",
        "year",
        "engine_type",
        "fuel_type",
        "description",
    ]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description"]
    list_editable = ["description"]


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    readonly_fields = ["id"]
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ["date", "car", "total_price", "status", "deadline", "user"]
    list_editable = ["status"]
    inlines = [OrderLineInline]


admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
