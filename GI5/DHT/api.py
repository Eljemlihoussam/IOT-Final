from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.utils.dateparse import parse_date
from django.conf import settings
from django.core.mail import send_mail
from .utils import send_telegram, send_call_alert
from twilio.rest import Client


# ============================================================
# ===============   GET DATA WITH DATE FILTER  ===============
# ============================================================

@api_view(['GET'])
def Dlist(request):
    """
    Retourne les données du capteur DHT11.
    Si start et end sont fournis :
    /api/?start=2025-01-01&end=2025-01-20
    Alors les données sont filtrées entre ces deux dates.
    """

    start = request.GET.get("start", None)
    end = request.GET.get("end", None)

    queryset = Dht11.objects.all().order_by("dt")

    # Filtre début
    if start:
        start_date = parse_date(start)
        if start_date:
            queryset = queryset.filter(dt__date__gte=start_date)

    # Filtre fin
    if end:
        end_date = parse_date(end)
        if end_date:
            queryset = queryset.filter(dt__date__lte=end_date)

    serialized = DHT11serialize(queryset, many=True).data
    return Response({"data": serialized})


# ============================================================
# =====================   POST DATA   ========================
# ============================================================

class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        instance = serializer.save()
        temp = instance.temp

        # ============= Alertes si température trop élevée =============
        if temp > 20:  # SEUIL configurable
            # 1) EMAIL ALERT
            try:
                send_mail(
                    subject="⚠️ Alerte Température élevée",
                    message=f"La température a atteint {temp:.1f} °C à {instance.dt}.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=["eljemli.houssameddine.24@ump.ac.ma"],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Erreur lors de l'envoi de l'email : {e}")

            # 2) TELEGRAM ALERT
            alert_msg = f"⚠️ Alerte DHT11: {temp:.1f} °C (>20) à {instance.dt}"
            send_telegram(alert_msg)

            # 3) APPEL TÉLÉPHONIQUE (TWILIO)
            try:
                send_call_alert(alert_msg)
            except Exception as exc:
                print(f"Twilio non configuré ou erreur d'appel: {exc}")
