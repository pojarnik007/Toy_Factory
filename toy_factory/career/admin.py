from django.contrib import admin
from .models import Vacancy

@admin.register(Vacancy)
class AdminVacancy(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )
