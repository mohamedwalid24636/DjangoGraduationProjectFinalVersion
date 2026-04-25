from django.conf import settings
from twilio.rest import Client as TwilioClient

def trigger_emergency_protocol(user, crisis_note):
    from ..models import Alert, EmergencyContact
    alert = Alert.objects.create(
        user=user,
        message=f"🚨 High Risk Detected: {crisis_note}",
        type='emergency'
    )
    
    contacts = EmergencyContact.objects.filter(user=user)
    if contacts.exists():
        try:
            twilio_client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            for contact in contacts:
                twilio_client.messages.create(
                    body=f"Emergency Alert for {user.first_name}: {crisis_note}. Please check on them.",
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=str(contact.phone)
                )
        except Exception as e:
            print(f"Twilio SMS Error: {e}")