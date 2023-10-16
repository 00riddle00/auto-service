from django.contrib import admin
from .models import CarModel, Car, Service, Order, OrderLine


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('service', 'order', 'quantity', 'price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'car', 'sum')
    list_editable = ('car', 'sum')


class CarAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'car_model', 'vin_code', 'client')
    list_filter = ('client', 'car_model')
    search_fields = ('plate_number', 'vin_code')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
