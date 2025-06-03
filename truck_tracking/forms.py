from django import forms
from .models import Truck

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['doc_guid', 'doc_date', 'license_plate', 'driver_name', 'driver_phone', 'status', 'arrival_time']
        widgets = {
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'doc_date': forms.DateInput(attrs={'type': 'date'}),
        }