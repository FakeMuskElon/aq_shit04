from django.db import models
import requests
from django.conf import settings

class Truck(models.Model):
    STATUS_CHOICES = [
        ('AWAITING_ARRIVAL', 'Ожидает'),
        ('ARRIVED', 'Приехал'),
        ('ON_TERRITORY', 'Заехал на территорию'),
        ('LOADING', 'На погрузке'),
        ('LOADED', 'Загружен'),
        ('DEPARTED', 'Выехал'),
    ]

    doc_guid = models.CharField(max_length=128, unique=True, verbose_name='Идентификатор документа')
    doc_date = models.DateField(null=True, blank=True, verbose_name='Дата документа')
    driver_name = models.CharField(max_length=100, verbose_name='Имя водителя')
    driver_phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон водителя')
    license_plate = models.CharField(max_length=20, verbose_name='Номерной знак')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AWAITING_ARRIVAL', verbose_name='Статус')
    arrival_time = models.DateTimeField(null=True, blank=True, verbose_name='Время прибытия')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return f"{self.license_plate} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        old_status = None
        if self.pk:
            try:
                old_instance = Truck.objects.get(pk=self.pk)
                old_status = old_instance.status
            except Truck.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        if old_status != self.status:
            status_map = {
                'AWAITING_ARRIVAL': 'awaiting',
                'ARRIVED': 'arrived',
                'ON_TERRITORY': 'on_territory',
                'LOADING': 'loading',
                'LOADED': 'loaded',
                'DEPARTED': 'departed',
            }
            new_status = status_map.get(self.status, 'awaiting')
            payload = {
                'DocGUID': self.doc_guid,
                'TruckStatus': new_status
            }
            try:
                response = requests.post(settings.TRUCK_STATUS_API_URL, json=payload)
                response.raise_for_status()
                print(f"Sent POST for DocGUID {self.doc_guid} with status {new_status}: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error sending POST for DocGUID {self.doc_guid}: {e}")

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорт'

class DrivingSlot(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE, related_name='loading_slots', verbose_name='Транспорт')
    gate = models.CharField(max_length=10, verbose_name='Ворота')
    uploading_at = models.DateTimeField(null=True, blank=True, verbose_name='Время погрузки')
    store = models.CharField(max_length=100, blank=True, verbose_name='Склад')

    def __str__(self):
        return f"Slot for {self.truck} at {self.gate}"

    class Meta:
        verbose_name = 'Слот погрузки'
        verbose_name_plural = 'Слоты погрузки'