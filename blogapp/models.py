from django.db import models
from authapp.models import SNUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
from django.contrib.contenttypes.fields import GenericRelation

NULLABLE = {'blank': True, 'null': True}


class SNSections(models.Model):
    """Разделы"""
    name = models.CharField(max_length=64, unique=True, verbose_name='Название раздела')
    title = models.CharField(max_length=30, verbose_name='Title раздела')
    description = models.TextField(verbose_name='Описание раздела')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class LikeDislikeManager(models.Manager):
    """Менеджер лайков"""
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def articles(self):
        return self.get_queryset().filter(content_type__model='article').order_by('-articles__pub_date')

    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__pub_date')


class LikeDislike(models.Model):
    """Лайки"""
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(SNUser, verbose_name="Пользователь", on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class SNPosts(models.Model):
    """Посты"""
    section = models.ForeignKey(SNSections, on_delete=models.CASCADE, verbose_name='Раздел поста', **NULLABLE)
    user = models.ForeignKey(SNUser, on_delete=models.CASCADE, verbose_name='Автор')
    name = models.CharField(max_length=128, verbose_name='Заголовок поста')
    image = models.ImageField(upload_to='posts', blank=True, null=True, verbose_name='Превьюшка поста')
    text = models.TextField(verbose_name='Текст поста')
    short_desc = models.CharField(max_length=255, verbose_name='Краткое описание поста')
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    votes = GenericRelation(LikeDislike, related_query_name='articles')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comments(models.Model):
    """Комментарии"""
    user = models.ForeignKey(SNUser, on_delete=models.CASCADE, verbose_name='Комментатор')
    post = models.ForeignKey(SNPosts, on_delete=models.CASCADE, verbose_name='Пост')
    text = models.CharField(max_length=1000, verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, db_index=True)
    votes = GenericRelation(LikeDislike, related_query_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class SNSubscribe(models.Model):
    """Подписки пользователя"""
    user = models.ForeignKey(SNUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    section = models.ForeignKey(SNSections, on_delete=models.CASCADE, verbose_name='Раздел на который он подписан')
