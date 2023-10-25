from time import sleep
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_feedback_email_task(email_address):

    #sleep(10)
    send_mail('feedback', 'thanks', 'support@ex.com', [email_address], fail_silently=False)


@shared_task
def print_something_terminal(message):
    sleep(1)
    print(message)
    return message
