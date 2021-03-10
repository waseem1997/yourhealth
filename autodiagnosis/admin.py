from django.contrib import admin

from .models import Gender, Origin, Symptom, Correlated_Report, Report

# Register your models here.

admin.site.register(Gender)
admin.site.register(Origin)
admin.site.register(Symptom)
admin.site.register(Report)
admin.site.register(Correlated_Report)
