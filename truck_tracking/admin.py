from django.contrib import admin
from .models import Truck, DrivingSlot

@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ('doc_guid', 'doc_date', 'license_plate', 'driver_name', 'driver_phone', 'status', 'arrival_time', 'updated_at')
    list_filter = ('status',)
    search_fields = ('doc_guid', 'license_plate', 'driver_name', 'driver_phone')

@admin.register(DrivingSlot)
class DrivingSlotAdmin(admin.ModelAdmin):
    list_display = ('truck', 'gate', 'uploading_at', 'store')
    list_filter = ('gate',)
    search_fields = ('truck__doc_guid', 'gate', 'store')