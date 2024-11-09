# Generated by Django 4.1.13 on 2024-11-08 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('matricula', models.CharField(max_length=9, primary_key=True, serialize=False, unique=True, verbose_name='Matricula')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo')),
                ('nombres', models.CharField(max_length=100, verbose_name='Nombres')),
                ('apellido_paterno', models.CharField(max_length=30, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(blank=True, max_length=30, null=True, verbose_name='Apellido Materno')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
