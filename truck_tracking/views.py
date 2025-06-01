import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.dateparse import parse_datetime, parse_date
from .models import Truck
from .forms import TruckForm

def fetch_truck_data():
    try:
        response = requests.get('http://127.0.0.1:5001/truck_info')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching truck data: {e}")
        return []

def sync_trucks():
    truck_data = fetch_truck_data()
    status_map = {
        'awaiting': 'AWAITING_ARRIVAL',
        'ready': 'READY_TO_ENTER',
        'on_territory': 'ON_TERRITORY',
        'loading': 'LOADING',
        'loaded': 'LOADED',
        'departed': 'DEPARTED',
    }
    for data in truck_data:
        arrival_time = parse_datetime(data.get('ArrivalDateTime', '')) if data.get('ArrivalDateTime') else None
        doc_date = parse_date(data.get('DocDate', '')) if data.get('DocDate') else None
        status = status_map.get(data.get('TruckStatus', '').lower(), 'AWAITING_ARRIVAL')
        Truck.objects.update_or_create(
            doc_guid=data.get('DocGUID'),
            defaults={
                'doc_date': doc_date,
                'driver_name': data.get('TruckDriver_name', ''),
                'license_plate': data.get('TruckLicense_plate', ''),
                'status': status,
                'arrival_time': arrival_time,
                'gate': data.get('Gate', ''),
            }
        )

def truck_list(request):
    sync_trucks()  # Синхронизация данных при каждом запросе
    query = request.GET.get('q', '')
    trucks = Truck.objects.all()
    if query:
        trucks = trucks.filter(
            Q(doc_guid__icontains=query) |
            Q(doc_date__icontains=query) |
            Q(license_plate__icontains=query) |
            Q(driver_name__icontains=query) |
            Q(status__icontains=query) |
            Q(arrival_time__icontains=query) |
            Q(gate__icontains=query)
        )
    trucks = trucks.order_by('-updated_at')
    return render(request, 'truck_tracking/truck_list.html', {'trucks': trucks, 'query': query})

@login_required
def truck_create(request):
    if request.method == 'POST':
        form = TruckForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('truck_list')
    else:
        form = TruckForm()
    return render(request, 'truck_tracking/truck_form.html', {'form': form})

@login_required
def truck_update(request, pk):
    truck = get_object_or_404(Truck, pk=pk)
    if request.method == 'POST':
        form = TruckForm(request.POST, instance=truck)
        if form.is_valid():
            form.save()
            return redirect('truck_list')
    else:
        form = TruckForm(instance=truck)
    return render(request, 'truck_tracking/truck_form.html', {'form': form})

@login_required
def truck_delete(request, pk):
    truck = get_object_or_404(Truck, pk=pk)
    if request.method == 'POST':
        truck.delete()
        return redirect('truck_list')
    return render(request, 'truck_tracking/truck_confirm_delete.html', {'truck': truck})