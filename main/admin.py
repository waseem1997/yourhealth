from django.contrib import admin

from .models import Clinic, Appointment, Article, Category, News

# Register your models here.

admin.site.register(Clinic)
admin.site.register(Appointment)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(News)
