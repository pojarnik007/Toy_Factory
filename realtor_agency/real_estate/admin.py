from django.contrib import admin
from .models import RealEstateObject, ObjectCategory, Sale


@admin.register(RealEstateObject)
class AdminRealEstateObject(admin.ModelAdmin):
    list_filter = ('price', 'category')
    search_fields = ('title', 'location')


@admin.register(ObjectCategory)
class AdminObjectCategory(admin.ModelAdmin):
    pass

@admin.register(Sale)
class AdminSale(admin.ModelAdmin):
    list_filter = ('sale_date', 'client')