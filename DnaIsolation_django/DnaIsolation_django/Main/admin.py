from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Company)
admin.site.register(models.Order)
admin.site.register(models.Material)
admin.site.register(models.LinkedFile)