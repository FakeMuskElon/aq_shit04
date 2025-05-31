from django.db import models

class Truck(models.Model):
    STATUS_CHOICES = [
        ('AWAITING_ARRIVAL', 'Ожидает прибытия'),
        ('READY_TO_ENTER', 'Готов к заезду'),
        ('ON_TERRITORY', 'Заехал на территорию'),
        ('LOADING', 'В процессе погрузки'),
        ('LOADED', 'Погружен'),
        ('DEPARTED', 'Выехал в рейс'),
    ]

    license_plate = models.CharField(max_length=20, unique=True, verbose_name='Номерной знак')
    driver_name = models.CharField(max_length=100, verbose_name='Имя водителя')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AWAITING_ARRIVAL', verbose_name='Статус')
    arrival_time = models.DateTimeField(null=True, blank=True, verbose_name='Время прибытия')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return f"{self.license_plate} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорт'
