from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


def send_verify_email(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activate_key])
    full_link = f'{settings.DOMAIN_NAME}{verify_link}'

    message = f'Для активации учетной записи {user.username} на сайте' \
              f' {settings.DOMAIN_NAME} перейдите по ссылке {full_link}'

    return send_mail(
        'Активация аккаунта на сайте SCI.NET',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )


# def send_message_all_moderators(message):