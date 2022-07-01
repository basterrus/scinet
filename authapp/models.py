from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

NULLABLE = {'blank': True, 'null': True}


class SNUser(AbstractUser):
    """Профиль пользователя"""
    avatar = models.ImageField(upload_to='users_avatars', verbose_name='Аватар', **NULLABLE)
    patronymic = models.CharField(max_length=150, verbose_name='Отчество', **NULLABLE)
    age = models.PositiveSmallIntegerField(verbose_name='Возраст', **NULLABLE)
    is_moderator = models.BooleanField(default=False, verbose_name='Модератор')
    is_superuser = models.BooleanField(default=False, verbose_name='Администратор')

    user_blocked = models.BooleanField(default=False, verbose_name='Заблокирован')
    date_blocked_end = models.DateTimeField(blank=True, null=True)

    activate_key = models.CharField(max_length=128, verbose_name='Ключ активации', blank=True, null=True)
    activate_key_expired = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activate_key_expired + timedelta(hours=48):
            return True
        return False

    def activate_user(self):
        self.is_active = True
        self.activate_key = None
        self.activate_key_expired = None

        self.save()


class SNUserProfile(models.Model):
    """Дополнительна информация из профиля пользователя"""
    MALE = 'M'
    FEMALE = 'W'
    OTHERS = 'O'

    GENDERS = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
        (OTHERS, 'Иное'),
    )

    user = models.OneToOneField(SNUser, null=False, unique=True, on_delete=models.CASCADE, db_index=True)
    about_me = models.TextField(verbose_name='Обо мне', **NULLABLE)
    gender = models.CharField(choices=GENDERS, default=OTHERS, verbose_name='Пол', max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @receiver(post_save, sender=SNUser)
    def create_user_profile(sender, instance, created, **kwargs):
        """Сигнал на создание профиля"""
        if created:
            SNUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=SNUser)
    def update_user_profile(sender, instance, created, **kwargs):
        """Сигнал на обновление профиля"""
        instance.snuserprofile.save()
