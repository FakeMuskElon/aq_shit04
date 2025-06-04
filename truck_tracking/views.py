import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.dateparse import parse_datetime, parse_date
from django.conf import settings
from .models import Truck, DrivingSlot
from .forms import TruckForm
from requests.auth import HTTPBasicAuth

def fetch_truck_data():
    try:
        response = requests.get(
            settings.TRUCK_INFO_API_URL,
            auth=HTTPBasicAuth(settings.TRUCK_INFO_API_USERNAME, settings.TRUCK_INFO_API_PASSWORD),
            verify=False  # Временное отключение проверки SSL для localhost
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching truck data: {e}")
        return []

def sync_trucks():
    truck_data = fetch_truck_data()
    status_map = {
        'ожидает приезда': 'AWAITING_ARRIVAL',
        'приехал': 'ARRIVED',
        'заехал на территорию': 'ON_TERRITORY',
        'на погрузке': 'LOADING',
        'загружен': 'LOADED',
        'выехал': 'DEPARTED',
    }
    seen_guids = set()
    for data in truck_data:
        doc_guid = data.get('doc_guid')
        if not doc_guid:
            print(f"Skipping entry with missing doc_guid: {data}")
            continue
        if doc_guid in seen_guids:
            print(f"Duplicate doc_guid found in JSON: {doc_guid}")
            continue
        seen_guids.add(doc_guid)

        driver_name = data.get('driver_name', '').strip() or ''
        driver_phone = data.get('driver_phone', '').strip() or ''
        license_plate = data.get('license_plate', '').strip() or ''
        arrival_time = parse_datetime(data.get('arrival_time', '')) if data.get('arrival_time') else None
        doc_date = parse_date(data.get('doc_date', '')) if data.get('doc_date') else None
        status = status_map.get(data.get('status', '').lower(), 'AWAITING_ARRIVAL')

        try:
            truck, created = Truck.objects.get_or_create(doc_guid=doc_guid)
            if created or driver_name:
                truck.driver_name = driver_name
            if created or driver_phone:
                truck.driver_phone = driver_phone
            if created or license_plate:
                truck.license_plate = license_plate
            if created or doc_date:
                truck.doc_date = doc_date
            if created or status:
                truck.status = status
            if created or arrival_time:
                truck.arrival_time = arrival_time
            truck.save()

            # Обработка loading_slots
            DrivingSlot.objects.filter(truck=truck).delete()  # Удаляем старые слоты
            for slot_data in data.get('loading_slots', []):
                uploading_at = parse_datetime(slot_data.get('uploading_at', '')) if slot_data.get('uploading_at') else None
                DrivingSlot.objects.create(
                    truck=truck,
                    gate=slot_data.getrikes('gate', '').strip() or '',
                    uploading_at= uploading_at, #upgrading_at,
                    store=slot_data.get('store', '').strip() or ''
                )

            print(f"{'Created' if created else 'Updated'} truck: {doc_guid}, driver_name: {truck.driver_name}")
        except Exception as e:
            print(f"Error processing truck with doc_guid: {e}")

def truck_list(request):
    sync_trucks()
    query = request.GET.get('q', '')
    trucks = Truck.objects.all()
    if query:
        trucks = trucks.filter(
            Q(doc_guid__icontains=query) |
            Q(doc_date__icontains=query) |
            Q(license_plate__icontains=query) |
            Q(driver_name__icontains=query) |
            Q(driver_phone__icontains=query) |
            Q(status__icontains=query) |
            Q(arrival_time__icontains=query) |
            Q(loading_slots__gate__icontains=query) |
            Q(loading_slots__store__icontains=query)
        ).distinct()
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