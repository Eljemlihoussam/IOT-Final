import requests
from django.conf import settings
from twilio.rest import Client
def send_telegram(text: str) -> bool:
    """Envoie un message Telegram via l'API officielle. Retourne True si OK."""
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        r = requests.post(url, data={"chat_id": chat_id, "text": text})
        return r.ok
    except Exception:
        return False


def send_call_alert(temp):
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)

    call = client.calls.create(
        twiml=f'<Response><Say>Attention, la température est de {temp} degrés, seuil dépassé !</Say></Response>',
        to='+',  # Numéro à appeler
        from_=''  # Numéro Twilio
    )
    print(call.sid)