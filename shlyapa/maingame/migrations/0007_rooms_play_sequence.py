# Generated by Django 5.0.2 on 2024-04-15 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maingame', '0006_remove_rooms_test_remove_words_test_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='play_sequence',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
