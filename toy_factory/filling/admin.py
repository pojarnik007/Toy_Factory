from django.contrib import admin


from .models import FAQ, Article, CompanyInformation



@admin.register(CompanyInformation)
class AdminCompanyInformation(admin.ModelAdmin):
    pass


@admin.register(FAQ)
class AdminFAQ(admin.ModelAdmin):
    list_display = ('question', )
    search_fields = ('question', )


@admin.register(Article)
class AdminArticle(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', )

# filling/admin.py

from django.contrib import admin
from .models import CompanyInformation, CompanyHistory, Partner, FAQ, Article

# Регистрируем все модели, чтобы ими можно было управлять

@admin.register(CompanyHistory)
class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ('year', 'event')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website') # Что показывать в списке партнеров
    search_fields = ('name',) # По каким полям искать
# filling/admin.py

from django.contrib import admin
from .models import CompanyInformation, CompanyHistory, Partner, FAQ, Article, SliderSettings, PromoSlide


@admin.register(SliderSettings)
class SliderSettingsAdmin(admin.ModelAdmin):
    # Запрещаем создавать больше 1 настройки, чтобы не путаться
    def has_add_permission(self, request):
        return not SliderSettings.objects.exists()

@admin.register(PromoSlide)
class PromoSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)