# Generated by Django 5.0.1 on 2024-04-01 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_habit_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='habit',
            name='weekly_rate',
            field=models.IntegerField(blank=True, default=7),
        ),
        migrations.AddField(
            model_name='progress',
            name='color',
            field=models.CharField(default='gray'),
        ),
    ]
