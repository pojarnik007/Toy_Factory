from django.contrib import admin

from reviews.models import Review

from .models import User

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    inlines = [ReviewInline]