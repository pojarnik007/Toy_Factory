from django.contrib import admin
from .models import ToyType, Toy, Client, Order, PromoCode, PickupPoint
from .models import Manufacturer

@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'toy_type', 'price', 'is_active', 'in_stock')
    list_filter = ('is_active', 'toy_type')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone', 'is_wholesale')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'toy', 'order_date', 'quantity', 'status')
    list_filter = ('order_date', 'client__city', 'status', 'toy__toy_type')



@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


admin.site.register(ToyType)
admin.site.register(PromoCode)
admin.site.register(PickupPoint)