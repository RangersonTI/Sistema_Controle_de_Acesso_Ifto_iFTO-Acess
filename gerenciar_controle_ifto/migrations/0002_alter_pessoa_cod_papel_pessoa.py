# Generated by Django 5.1.1 on 2024-09-09 02:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciar_controle_ifto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='cod_Papel_pessoa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gerenciar_controle_ifto.papel_pessoa'),
        ),
    ]
