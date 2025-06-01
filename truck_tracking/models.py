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

    doc_guid = models.CharField(max_length=50, unique=True, verbose_name='Идентификатор документа')
    doc_date = models.DateField(null=True, blank=True, verbose_name='Дата документа')
    driver_name = models.CharField(max_length=100, verbose_name='Имя водителя')
    license_plate = models.CharField(max_length=20, verbose_name='Номерной знак')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AWAITING_ARRIVAL', verbose_name='Статус')
    arrival_time = models.DateTimeField(null=True, blank=True, verbose_name='Время прибытия')
    gate = models.CharField(max_length=10, null=True, blank=True, verbose_name='Ворота')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        return f"{self.license_plate} ({self.get_status_display()})"

    class Meta:
        verbose_name = 'Транспорт'
        verbose_name_plural = 'Транспорт'
