# Generated by Django 4.0.3 on 2022-06-03 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_snposts'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SNPosts',
        ),
        migrations.DeleteModel(
            name='SNSections',
        ),
    ]