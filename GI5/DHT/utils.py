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
    # Si les identifiants ne sont pas configurés, on sort pour éviter un crash.
    account_sid = ''
    auth_token = ''
    to_number = ''
    from_number = ''
    if not account_sid or not auth_token or not to_number or not from_number:
        print("Twilio non configuré: appel ignoré.")
        return False

    try:
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            twiml=f'<Response><Say>Attention, la température est de {temp} degrés, seuil dépassé !</Say></Response>',
            to=to_number,
            from_=from_number
        )
        print(call.sid)
        return True
    except Exception as exc:
        print(f"Erreur Twilio: {exc}")
        return False