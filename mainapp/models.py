from django.db import models


class SNSections(models.Model):
    """Главные разделы"""
    name = models.CharField(max_length=64, unique=True, verbose_name='Название раздела')
    title = models.CharField(max_length=30, verbose_name='Title раздела')
    description = models.TextField(verbose_name='Описание раздела')
    is_active = models.BooleanField(default=True)

    # def __str__(self):
    #     return f'{self.name}'
    #
    # class Meta:
    #     verbose_name = 'Категория'
    #     verbose_name_plural = 'Категории'
    #     ordering = ('-id',)

