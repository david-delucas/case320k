from django.contrib import admin
from .models import BusinessCase

from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class BusinessCaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Main", {
            "fields": ["bc_name","bc_creation_datetime"]
        }),

        ("Content", {
                    "fields": ["bc_description"]

                })

    )
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    
admin.site.register(BusinessCase,BusinessCaseAdmin)