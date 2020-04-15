from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.
class BusinessCaseCategory(models.Model):
    bc_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    category_slug = models.CharField(max_length=200, default="cat1")

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.bc_category


class BusinessCaseSeries(models.Model):
    bc_series = models.CharField(max_length=200)

    bc_category = models.ForeignKey(BusinessCaseCategory, default=1, verbose_name="Category", on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)

    class Meta:
        # otherwise we get "Seriess in admin"
        verbose_name_plural = "Series"

    def __str__(self):
        return self.bc_series


class BusinessCase(models.Model):
    bc_name = models.CharField(max_length=200)
    bc_description = models.TextField()
    bc_creation_datetime = models.DateTimeField("Creation date", default=timezone.now())
    #https://docs.djangoproject.com/en/2.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
    bc_series = models.ForeignKey(BusinessCaseSeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
    bc_slug = models.CharField(max_length=200, default="bc1")

    def __str__(self):
        return self.bc_name

