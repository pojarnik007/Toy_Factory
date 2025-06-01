from django.contrib import admin
from .models import ToyType, ToyModel, Toy, Client, Order

@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'toy_type', 'price', 'is_active')
    list_filter = ('is_active', 'toy_type')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'phone')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'toy', 'order_date', 'quantity')
    list_filter = ('order_date', 'client__city')

admin.site.register(ToyType)
admin.site.register(ToyModel)
