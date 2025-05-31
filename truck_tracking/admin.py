from django.contrib import admin
from .models import Truck

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'driver_name', 'status', 'arrival_time', 'updated_at')
    list_filter = ('status',)
    search_fields = ('license_plate', 'driver_name')

