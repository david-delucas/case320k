from django.contrib import admin
from .models import BusinessCase, BusinessCaseCategory, BusinessCaseSeries

from tinymce.widgets import TinyMCE
from django.db import models

# Register your models here.

class BusinessCaseAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Main", {
            "fields": ["bc_name","bc_creation_datetime"]
        }),
        ("URL", {'fields': ["bc_slug"]}),
        ("Series", {'fields': ["bc_series"]}),
        ("Content", {
                    "fields": ["bc_description"]

                })

    )
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 80, 'rows': 30})},
    }

admin.site.register(BusinessCaseSeries)
admin.site.register(BusinessCaseCategory)
admin.site.register(BusinessCase,BusinessCaseAdmin)


