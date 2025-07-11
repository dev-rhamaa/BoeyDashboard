from django.shortcuts import render

from .models import SensorReading


import json

from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """Simple dashboard displaying latest 100 sensor readings."""

    readings_qs = SensorReading.objects.order_by("-timestamp")[:100]
    # Reverse queryset for chronological plotting (oldest -> newest)
    readings = list(reversed(readings_qs))
    latest = readings[-1] if readings else None
    summary = {
        "ph": getattr(latest, "ph", None),
        "turbidity_ntu": getattr(latest, "turbidity_ntu", None),
        "temperature_c": getattr(latest, "temperature_c", None),
    } if latest else {}

    # Prepare data for Chart.js
    labels = [r.timestamp.strftime("%H:%M:%S") for r in readings]
    ph_data = [r.ph for r in readings]
    turbidity_data = [r.turbidity_ntu for r in readings]
    temp_data = [r.temperature_c for r in readings]

    context = {
        "readings": readings_qs,  # keep latest first for table
        "summary": summary,
        "labels": json.dumps(labels),
        "ph_data": json.dumps(ph_data),
        "turbidity_data": json.dumps(turbidity_data),
        "temp_data": json.dumps(temp_data),
    }

    return render(request, "boey/dashboard.html", context)
