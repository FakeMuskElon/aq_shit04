from django.contrib import admin
from .models import Truck

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('doc_guid', 'doc_date', 'license_plate', 'driver_name', 'status', 'arrival_time', 'gate', 'updated_at')
    list_filter = ('status',)
    search_fields = ('doc_guid', 'doc_date', 'license_plate', 'driver_name', 'gate')

