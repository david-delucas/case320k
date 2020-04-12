from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.
class BusinessCase(models.Model):
    bc_name = models.CharField(max_length=200)
    bc_description = models.TextField()
    bc_creation_datetime = models.DateTimeField("Creation date", default=timezone.now())

    def __str__(self):
        return self.bc_name