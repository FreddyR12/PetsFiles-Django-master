# Generated by Django 4.1.3 on 2022-11-18 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veterinary', '0007_alter_client_email_alter_client_veterinary_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veterinary',
            name='direccion',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
