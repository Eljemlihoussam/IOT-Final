# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone

from .models import Dht11

def dashboard(request):
    # Rend juste la page; les données sont chargées via JS
    return render(request, "dashboard.html")

def graph_temp(request):
    return render(request, "graph_temp.html")

def graph_hum(request):
    return render(request, "graph_hum.html")


def latest_json(request):
    last = Dht11.objects.order_by('-dt').first()
    if not last:
        return JsonResponse({"detail": "no data"}, status=404)

    # Assure-toi que last.dt est aware
    if timezone.is_naive(last.dt):
        last_dt = timezone.make_aware(last.dt, timezone=timezone.utc)
    else:
        last_dt = last.dt

    now = timezone.now()
    elapsed_minutes = int((now - last_dt).total_seconds() // 60)

    return JsonResponse({
        "temperature": last.temp,
        "humidity": last.hum,
        "minutes_since_last": elapsed_minutes,
        "timestamp": last.dt.isoformat()
    })