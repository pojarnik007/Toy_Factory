from django.contrib import admin
from .models import PromoCode

@admin.register(PromoCode)
class AdminPromoCode(admin.ModelAdmin):
    list_display = ('text', 'discount_percent', 'state')
    search_fields = ('text', )
    list_filter = ('state',)