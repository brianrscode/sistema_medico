from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UsuarioManager(BaseUserManager):
    def create_user(self, matricula, nombres, email, password=None):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')

        usuario = self.model(
            matricula=matricula,
            nombres=nombres,
            email=self.normalize_email(email),
        )
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, matricula, nombres, email, password=None):
        usuario = self.create_user(
            matricula=matricula,
            nombres=nombres,
            email=email,
            password=password,
        )
        usuario.usuario_administrador = True
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractBaseUser):
    matricula = models.CharField('Matricula', max_length=9, primary_key=True, unique=True)
    email = models.EmailField('Correo', unique=True)
    nombres = models.CharField('Nombres', max_length=100)
    apellido_paterno = models.CharField('Apellido Paterno', max_length=30)
    apellido_materno = models.CharField('Apellido Materno', max_length=30, blank=True, null=True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['matricula', 'nombres']

    def __str__(self):
        return f'{self.matricula} - {self.nombres} - {self.is_staff}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador

    @property
    def is_superuser(self):
        return self.usuario_administrador

    def save(self, *args, **kwargs):
        if not self.matricula:
            self.usuario_activo = True
        super(Usuario, self).save(*args, **kwargs)
