# Generated by Django 4.0.4 on 2022-06-17 16:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogapp', '0008_snposts_is_moderated_alter_snposts_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField(db_index=True, default=False)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('mode', models.CharField(choices=[('L', 'Лайк'), ('C', 'Комментарий')], default='L', max_length=1, verbose_name='Вид уведомления')),
                ('notifier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Уведомитель')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogapp.snposts', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
            },
        ),
    ]
