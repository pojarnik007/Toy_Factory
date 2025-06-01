from django.contrib import admin
from .models import PromoCode

@admin.register(PromoCode)
class AdminPromoCode(admin.ModelAdmin):
    list_display = ('text', )
    search_fields = ('text', )
