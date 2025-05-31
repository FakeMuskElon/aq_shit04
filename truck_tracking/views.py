# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Truck
# from .forms import TruckForm

# def truck_list(request):
#     trucks = Truck.objects.all().order_by('-updated_at')
#     return render(request, 'truck_tracking/truck_list.html', {'trucks': trucks})

# def truck_create(request):
#     if request.method == 'POST':
#         form = TruckForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('truck_list')
#     else:
#         form = TruckForm()
#     return render(request, 'truck_tracking/truck_form.html', {'form': form})

# def truck_update(request, pk):
#     truck = get_object_or_404(Truck, pk=pk)
#     if request.method == 'POST':
#         form = TruckForm(request.POST, instance=truck)
#         if form.is_valid():
#             form.save()
#             return redirect('truck_list')
#     else:
#         form = TruckForm(instance=truck)
#     return render(request, 'truck_tracking/truck_form.html', {'form': form})

# def truck_delete(request, pk):
#     truck = get_object_or_404(Truck, pk=pk)
#     if request.method == 'POST':
#         truck.delete()
#         return redirect('truck_list')
#     return render(request, 'truck_tracking/truck_confirm_delete.html', {'truck': truck})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Truck
from .forms import TruckForm

def truck_list(request):
    trucks = Truck.objects.all().order_by('-updated_at')
    return render(request, 'truck_tracking/truck_list.html', {'trucks': trucks})

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