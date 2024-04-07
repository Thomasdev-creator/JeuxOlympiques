# Generated by Django 5.0.3 on 2024-04-07 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=240)),
                ('address_1', models.CharField(help_text='Adresse et numéro de rue.', max_length=240)),
                ('address_2', models.CharField(blank=True, help_text='Bâtiment, étage...', max_length=240)),
                ('city', models.CharField(max_length=1024)),
                ('zipcode', models.CharField(max_length=32)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
