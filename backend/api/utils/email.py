import logging
import threading
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

class EmailThread(threading.Thread):
    def __init__(self, subject, message, from_email, recipient_list, **kwargs):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.kwargs = kwargs
        # Ensure fail_silently is True to avoid unhandled thread exceptions crashing
        self.kwargs['fail_silently'] = True 
        super().__init__()

    def run(self):
        try:
            send_mail(
                self.subject,
                self.message,
                self.from_email,
                self.recipient_list,
                **self.kwargs
            )
            logger.info(f"Successfully sent background email to {self.recipient_list}")
        except Exception as e:
            logger.error(f"Failed to send background email to {self.recipient_list}. Error: {str(e)}")


def send_mail_async(subject, message, from_email, recipient_list, **kwargs):
    """
    Non-blocking, safe email sending utility using Threading.
    Use this in views to prevent Gunicorn worker timeouts on Railway.
    """
    EmailThread(subject, message, from_email, recipient_list, **kwargs).start()
