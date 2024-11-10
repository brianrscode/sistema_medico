# Generated by Django 4.1.13 on 2024-11-10 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('matricula', models.CharField(max_length=9, primary_key=True, serialize=False, unique=True, verbose_name='Matrícula')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo')),
                ('nombres', models.CharField(max_length=100, verbose_name='Nombres')),
                ('apellido_paterno', models.CharField(max_length=30, verbose_name='Apellido Paterno')),
                ('apellido_materno', models.CharField(blank=True, max_length=30, null=True, verbose_name='Apellido Materno')),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('medico', 'Médico'), ('paciente', 'Paciente'), ('admin', 'Administrador')], default='paciente', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistorialMedico',
            fields=[
                ('id_historial', models.CharField(max_length=9, primary_key=True, serialize=False, unique=True, verbose_name='Id Historial')),
                ('enfermedades_cronicas', models.CharField(blank=True, max_length=150, null=True, verbose_name='Enfermedades crónicas')),
                ('alergias', models.CharField(blank=True, max_length=150, null=True, verbose_name='Alergias')),
                ('medicamento_usado', models.CharField(blank=True, max_length=150, null=True, verbose_name='Medicamento usado')),
                ('es_embarazada', models.BooleanField(default=False)),
                ('usa_drogas', models.BooleanField(default=False)),
                ('usa_cigarro', models.BooleanField(default=False)),
                ('ingiere_alcohol', models.BooleanField(default=False)),
                ('paciente', models.OneToOneField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='historial', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
