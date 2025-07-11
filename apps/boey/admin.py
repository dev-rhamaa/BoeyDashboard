from django.contrib import admin

from .models import SensorReading


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = (
        "timestamp",
        "sensor_id",
        "ph",
        "turbidity_ntu",
        "do_mg_l",
        "ec_us_cm",
        "temperature_c",
        "latitude",
        "longitude",
    )
    list_filter = ("sensor_id",)
    search_fields = ("sensor_id",)

# Register your models here.
