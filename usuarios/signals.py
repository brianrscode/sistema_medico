from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from consultas.models import Consulta

from .models import Area, HistorialMedico, Role, Usuario


@receiver(post_migrate)
def crear_roles_por_defecto(sender, **kwargs):
    roles = ["paciente", "medico", "admin"]
    for role in roles:
        Role.objects.get_or_create(nombre_rol=role)


@receiver(post_migrate)
def crear_areas_por_defecto(sender, **kwargs):
    areas = [
        "Sistemas",
        "Bioquímica",
        "Mecatrónica",
        "Industrial",
        "Electromecánica",
        "Gastronomía",
        "Maestría",
        "Médico",
        "Administración",
        "Docente"
    ]
    for area in areas:
        Area.objects.get_or_create(carrera_o_puesto=area)


@receiver(post_migrate)
def crear_grupos_permisos(sender, **kwargs):
    # Crear grupos si no existen
    medico_group, _ = Group.objects.get_or_create(name="Medico")
    paciente_group, _ = Group.objects.get_or_create(name="Paciente")
    admin_group, _ = Group.objects.get_or_create(name="Administrador")

    # Definir permisos y grupos
    permisos_medico = [
        ('view_consulta', Consulta),
        ('add_consulta', Consulta),
        ('view_historialmedico', HistorialMedico),
        ('view_usuario', Usuario),
        ('change_usuario', Usuario),
    ]
    permisos_paciente = [
        ('view_consulta', Consulta),
        ('view_historialmedico', HistorialMedico),
        ('change_historialmedico', HistorialMedico),
        ('view_usuario', Usuario),
        ('change_usuario', Usuario),
    ]

    # Asignar permisos a los grupos
    def asignar_permisos(grupo, permisos):
        for permiso_codename, model in permisos:
            content_type = ContentType.objects.get_for_model(model)
            permission, _ = Permission.objects.get_or_create(codename=permiso_codename, content_type=content_type)
            grupo.permissions.add(permission)

    # Asignar permisos a cada grupo
    asignar_permisos(medico_group, permisos_medico)
    asignar_permisos(paciente_group, permisos_paciente)

    # Asignar todos los permisos al grupo Administrador
    all_permissions = Permission.objects.all()
    admin_group.permissions.set(all_permissions)


@receiver(post_save, sender=Usuario)
def asignar_grupo_y_crear_historial(sender, instance, created, **kwargs):
    if created:
        if instance.role == Role.objects.get(nombre_rol='medico'):
            medico_group = Group.objects.get(name='Medico')
            instance.groups.add(medico_group)
        elif instance.role == Role.objects.get(nombre_rol='paciente'):
            paciente_group = Group.objects.get(name='Paciente')
            instance.groups.add(paciente_group)
            if instance.carrera_o_puesto and instance.carrera_o_puesto != 'Médico':
                HistorialMedico.objects.create(id_historial=instance.clave, paciente=instance)
        elif instance.role == Role.objects.get(nombre_rol='admin'):
            admin_group = Group.objects.get(name='Administrador')
            instance.groups.add(admin_group)
        instance.save()
