from django.db import models
from usuarios.models import Usuario
from django.core.validators import RegexValidator


class Consulta(models.Model):
    id_consulta = models.BigAutoField(primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    padecimiento_actual = models.TextField()
    tratamiento_no_farmacologico = models.TextField('Tratamiento no farmacológico', max_length=100, blank=True, null=True)
    tratamiento_farmacologico_recetado = models.CharField('Tratamiento farmacológico recetado', max_length=100, blank=True, null=True)
    CHOICES = [("M", "Médica"), ("A", "Asesoría")]
    tipo_de_consulta = models.CharField('Tipo de consulta', max_length=1, choices=CHOICES, default="M")
    clave_paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='consultas_paciente',
        limit_choices_to={'role__nombre_rol': 'paciente'}
    )
    clave_medico = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='consultas_medico',
        limit_choices_to={'role__nombre_rol': 'medico'}
    )

    def __str__(self):
        return f"Consulta {self.id_consulta} - {self.fecha} - {self.clave_paciente} - {self.clave_medico}"


class SignosVitales(models.Model):
    id_signos = models.BigAutoField(primary_key=True)
    peso = models.DecimalField('Peso (kg)', max_digits=4, decimal_places=1, blank=True, null=True,
                               validators=[RegexValidator(
                                   regex=r'([4-9][0-9]|1[0-9][0-9])\.[0-9]',
                                   message='Formato de peso no valido'
                               )])  # en kg
    talla = models.DecimalField('Talla (m)', max_digits=4, decimal_places=2, blank=True, null=True,
                                validators=[RegexValidator(
                                    regex=r'(1\.[0-9][0-9]|2\.[0-2][0-9])',
                                    message='Formato de talla no valido'
                                )])  # en cm
    temperatura = models.DecimalField('Temperatura (°C)', max_digits=3, decimal_places=1, blank=True, null=True,
                                      validators=[RegexValidator(
                                          regex=r'(3[5-9]|4[0-3])\.[0-9]',
                                          message='Formato de temperatura no valido'
                                      )])  # en °C
    frecuencia_cardiaca = models.IntegerField('Frecuencia cardíaca (bpm)', blank=True, null=True,
                                              validators=[RegexValidator(
                                                  regex=r'(5[0-9]|[6-9][0-9]|100)',
                                                  message='Formato de frecuencia cardíaca no valido'
                                              )])  # en bpm
    frecuencia_respiratoria = models.IntegerField('Frecuencia respiratoria (rpm)', blank=True, null=True,
                                              validators=[RegexValidator(
                                                  regex=r'^(12|1[3-9]|2[0-9]|3[0-9]|40)$',
                                                  message='Formato de frecuencia cardíaca no valido'
                                              )])  # en rpm
    presion_arterial = models.CharField('Presión arterial', max_length=7, blank=True, null=True,
                                        validators=[RegexValidator(
                                            regex=r'\b(1[01][0-9]|120|12[0-9]|1[3-9][0-9]|140)\/(60|6[0-9]|70|7[0-9]|80|8[0-9]|90)\b',
                                            message='Formato de presión arterial no valido'
                                        )])  # ej: "120/80"
    consulta = models.OneToOneField(
        'Consulta',
        on_delete=models.CASCADE,
        related_name='signos_vitales'
    )

    def __str__(self):
        return f"{self.id_signos} - {self.consulta}"