from django.contrib import admin

from . import models

class LeadsAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['name']

admin.site.register(models.Lead, LeadsAdmin)