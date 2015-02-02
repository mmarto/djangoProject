from django.contrib import admin
from reportsViewer.models import Report, UserReport, Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Report)
admin.site.register(UserReport)
