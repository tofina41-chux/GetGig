import threading
from django.core.mail import send_mail
from django.conf import settings

def send_email_background(subject, message, recipient_list):
    """Sends an email on a separate system thread to prevent UI freezing."""
    thread = threading.Thread(
        target=send_mail,
        args=(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list),
        kwargs={'fail_silently': True}
    )
    thread.start()