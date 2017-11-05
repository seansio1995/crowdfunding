from django.contrib import admin
from .models import Person, Friend, Report
# Register your models here.
admin.site.register(Person)
admin.site.register(Friend)
#admin.site.register(Report)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass

