# Generated by Django 4.2.7 on 2025-05-08 00:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0002_alter_signosvitales_talla'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signosvitales',
            name='frecuencia_cardiaca',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(regex='(5[0-9]|[6-9][0-9]|100)')], verbose_name='Frecuencia cardíaca (bpm)'),
        ),
        migrations.AlterField(
            model_name='signosvitales',
            name='frecuencia_respiratoria',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.RegexValidator(regex='^(12|1[3-9]|2[0-9]|3[0-9]|40)$')], verbose_name='Frecuencia respiratoria (rpm)'),
        ),
        migrations.AlterField(
            model_name='signosvitales',
            name='peso',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.RegexValidator(regex='([4-9][0-9]|1[0-9][0-9])(\\.[0-9])?')], verbose_name='Peso (kg)'),
        ),
        migrations.AlterField(
            model_name='signosvitales',
            name='presion_arterial',
            field=models.CharField(blank=True, max_length=7, null=True, validators=[django.core.validators.RegexValidator(regex='\\b(1[01][0-9]|120|12[0-9]|1[3-9][0-9]|140)\\/(60|6[0-9]|70|7[0-9]|80|8[0-9]|90)\\b')], verbose_name='Presión arterial'),
        ),
        migrations.AlterField(
            model_name='signosvitales',
            name='talla',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.RegexValidator(regex='^(1\\.\\d{1,2}|2\\.[0-2]\\d?)')], verbose_name='Talla (m)'),
        ),
        migrations.AlterField(
            model_name='signosvitales',
            name='temperatura',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.RegexValidator(regex='(3[5-9]|4[0-3])(\\.[0-9])?')], verbose_name='Temperatura (°C)'),
        ),
    ]
