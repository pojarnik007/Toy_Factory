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

   