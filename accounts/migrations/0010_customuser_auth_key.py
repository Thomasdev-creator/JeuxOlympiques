# Generated by Django 5.0.3 on 2024-04-10 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_shippingaddress_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='auth_key',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
