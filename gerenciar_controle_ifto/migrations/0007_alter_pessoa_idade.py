# Generated by Django 5.1.1 on 2024-09-09 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciar_controle_ifto', '0006_alter_rfid_data_desativacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='idade',
            field=models.IntegerField(),
        ),
    ]
