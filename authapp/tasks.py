from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from celery import shared_task
from authapp.models import SNUser


@shared_task
def send_feedback_to_email(message_body: str, message_from: int = None) -> None:
    if message_from is not None:
        user_from = SNUser.objects.filter(pk=message_from).first().get_full_name()
    else:
        user_from = 'Аноним'

    send_mail(
        subject=f"Feedback from: {user_from}",
        message=message_body,
        recipient_list=['support@mail.com'],
        from_email='noreply@mail.com',
        fail_silently=False
    )


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activate_key])
    full_link = f'{settings.DOMAIN_NAME}{verify_link}'
    print(settings.DOMAIN_NAME)
    message = f'Ссылка для активации вашей учетной записи:  {full_link}'

    return send_mail(
        'Account activation',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
