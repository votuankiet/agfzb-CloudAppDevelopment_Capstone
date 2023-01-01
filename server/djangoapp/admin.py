from django.contrib import admin

from djangoapp.models import CarModel, CarMake


# from .models import related models


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2


# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    search_fields = ['name', 'type']


# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]


# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
