from django.contrib import admin

from .models import *

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee','date_joined']


class AttendenceAdmin(admin.ModelAdmin):
    list_display = ['employee','created_at']


admin.site.register(Company)
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(Attendence,AttendenceAdmin)

