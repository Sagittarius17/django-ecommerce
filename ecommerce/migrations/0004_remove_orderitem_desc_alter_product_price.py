# Generated by Django 4.1.1 on 2023-09-01 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_alter_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='desc',
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
