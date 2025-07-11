from django.db import models

class SensorReading(models.Model):
    """Represents one reading received via MQTT."""

    timestamp = models.DateTimeField(help_text="Timestamp embedded in the MQTT payload")
    sensor_id = models.CharField(max_length=100)
    ph = models.FloatField(help_text="pH value of the water")
    turbidity_ntu = models.FloatField(help_text="Turbidity (NTU)")
    do_mg_l = models.FloatField(help_text="Dissolved oxygen (mg/L)")
    ec_us_cm = models.FloatField(help_text="Electrical conductivity (µS/cm)")
    temperature_c = models.FloatField(help_text="Water temperature (°C)")
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.sensor_id} @ {self.timestamp}"
