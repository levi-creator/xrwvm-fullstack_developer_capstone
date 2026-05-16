from django.contrib import admin
from .models import CarMake, CarModel

# Inline class to show CarModels directly under CarMake in admin
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # how many empty rows to display for quick adds


# Admin class for CarMake
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [CarModelInline]


# Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'type', 'year')
    list_filter = ('car_make', 'type', 'year')
    search_fields = ('name', 'car_make__name')


# Register models with their respective admins
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
