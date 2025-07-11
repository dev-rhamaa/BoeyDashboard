from django.shortcuts import render

from .models import SensorReading


def dashboard(request):
    """Simple dashboard displaying latest 100 sensor readings."""

    readings = SensorReading.objects.all()[:100]
    return render(request, "boey/dashboard.html", {"readings": readings})
