# Generated by Django 5.0.3 on 2024-04-09 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_ticket_stripe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='slug',
            field=models.SlugField(blank=True, max_length=128),
        ),
    ]
