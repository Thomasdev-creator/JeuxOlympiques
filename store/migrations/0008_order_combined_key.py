# Generated by Django 5.0.3 on 2024-04-11 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_order_key_after_success_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='combined_key',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]