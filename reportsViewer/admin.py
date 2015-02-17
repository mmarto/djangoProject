from django.contrib import admin
from reportsViewer.models import Report, ReportArchive, UserReport, UserReportArch, RequestReport, Category

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),
                            'dir': ('name',),
                            'archive_dir': ('name',)}

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Report)
admin.site.register(ReportArchive)
admin.site.register(UserReport)
admin.site.register(UserReportArch)
admin.site.register(RequestReport)
