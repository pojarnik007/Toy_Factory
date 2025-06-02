from django.contrib import admin
from .models import Review

@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    list_display = ('title', 'rating', 'time')
    search_fields = ('title', )
    list_filter = ('rating', 'time',)
