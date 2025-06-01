from django import forms
from .models import Truck

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck
        fields = ['doc_guid', 'doc_date', 'license_plate', 'driver_name', 'status', 'arrival_time', 'gate']
        widgets = {
            'arrival_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'doc_date': forms.DateInput(attrs={'type': 'date'}),
        }