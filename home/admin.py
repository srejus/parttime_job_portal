from django.contrib import admin
from .models import Support


class SupportAdmin(admin.ModelAdmin):
    list_display = ['full_name','company','desc','created_at']

# Register your models here.
admin.site.register(Support,SupportAdmin)
