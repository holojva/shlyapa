# Generated by Django 5.0.2 on 2024-04-15 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maingame', '0005_words_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rooms',
            name='test',
        ),
        migrations.RemoveField(
            model_name='words',
            name='test',
        ),
        migrations.AddField(
            model_name='rooms',
            name='room_started',
            field=models.TimeField(null=True),
        ),
    ]