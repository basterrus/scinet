from django.db import models
from authapp.models import SNUser


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


class SNPosts(models.Model):
    """Таблица постов"""
    section = models.ForeignKey(SNSections, on_delete=models.CASCADE, verbose_name='Раздел поста')
    user = models.ForeignKey(SNUser, on_delete=models.CASCADE, verbose_name='Раздел поста')
    name = models.CharField(max_length=128, verbose_name='Название поста')
    image = models.ImageField(upload_to='posts', blank=True, null=True, verbose_name='Превьюшка поста')
    text = models.TextField(verbose_name='Текст поста')
    short_desc = models.CharField(max_length=255, verbose_name='Краткое описание поста')
    description = models.TextField(verbose_name='Описание поста')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
