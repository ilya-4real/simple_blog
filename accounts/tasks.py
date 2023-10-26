from celery import shared_task
from celery.utils.log import get_task_logger

from .services.email import send_welcome_email
from .services.image_resize import resize_image


logger = get_task_logger(__name__)


@shared_task
def send_welcome_email_task(email_address, username):
    logger.info('sent welcome email')
    return send_welcome_email(username, email_address)


@shared_task
def resize_profile_image(image_path):
    logger.info('image resizing')
    return resize_image(image_path)

