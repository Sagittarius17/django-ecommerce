# Generated by Django 4.1.1 on 2023-09-06 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_delete_customuser_rename_name_customer_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]