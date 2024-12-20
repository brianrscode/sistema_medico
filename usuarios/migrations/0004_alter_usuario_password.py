# Generated by Django 4.1.13 on 2024-12-06 03:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_usuario_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='password',
            field=models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(message='La contraseña debe tener al entre 8 y 15 caracteres, incluir una letra mayúscula, un número y un caracter especial.', regex='^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)(?=.*[@$!%*#?&ñ_])[A-Za-z\\d@$!%*#?&ñ_]{8,15}$')], verbose_name='Contraseña'),
        ),
    ]
