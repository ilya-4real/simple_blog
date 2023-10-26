from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def send_welcome_email(username: str, email: str):
    """
    function that generates an email
    :param username: username
    :param email: user email
    :return:
    """
    context = {
        'username': username,
        'email': email,
    }

    email_subject = f'Welcome to our service, {username.capitalize()}'
    email_body = render_to_string('email_message.txt', context)

    email_instance = EmailMessage(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, [email, ])

    return email_instance.send(fail_silently=False)
