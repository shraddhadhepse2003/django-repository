# Generated by Django 5.0.7 on 2024-09-03 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dj_app', '0003_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
