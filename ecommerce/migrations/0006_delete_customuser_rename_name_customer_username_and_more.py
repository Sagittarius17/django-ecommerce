# Generated by Django 4.1.1 on 2023-09-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='name',
            new_name='username',
        ),
        migrations.AddField(
            model_name='customer',
            name='full_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='phn_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
