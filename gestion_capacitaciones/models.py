from django.db import models

# Create your models here.
class Docente(models.Model):
    nombre = models.CharField(max_length=150)
    puesto = models.CharField(max_length=150)
    unidad_facultad = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre


class Capacitacion(models.Model):
    class Localidad(models.TextChoices):
        NACIONAL = "NACIONAL", "Nacional"
        INTERNACIONAL = "INTERNACIONAL", "Internacional"

    class Modalidad(models.TextChoices):
        PRESENCIAL = "PRESENCIAL", "Presencial"
        VIRTUAL = "VIRTUAL", "Virtual"

    tipo = models.CharField(max_length=100)
    proveedor = models.CharField(max_length=150)
    contacto = models.CharField(max_length=150, blank=True)
    localidad = models.CharField(
        max_length=20,
        choices=Localidad.choices,
    )
    modalidad = models.CharField(
        max_length=20,
        choices=Modalidad.choices,
    )
    nombre_evento = models.CharField(max_length=200)
    lugar = models.CharField(max_length=200, blank=True)

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    horario = models.CharField(max_length=100, blank=True)
    horas_totales = models.DecimalField(
        max_digits=7,
        decimal_places=2,
    )

    codigo_proyecto = models.CharField(max_length=100, blank=True)
    area_formacion = models.CharField(max_length=150, blank=True)

    costo_publicado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    inversion_honorarios = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    inversion_materiales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    viaticos_alimentacion = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    gastos_transporte = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    gastos_alojamiento = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    observaciones = models.TextField(blank=True)

    docentes = models.ManyToManyField(
        Docente,
        through="Participacion",
        related_name="capacitaciones",
    )

    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_evento

    @property
    def total_inversion(self):
        return (
            self.inversion_honorarios
            + self.inversion_materiales
            + self.viaticos_alimentacion
            + self.gastos_transporte
            + self.gastos_alojamiento
        )


class Participacion(models.Model):
    class EstadoAsistencia(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ASISTIO = "ASISTIO", "Asistió"
        AUSENTE = "AUSENTE", "Ausente"

    capacitacion = models.ForeignKey(
        Capacitacion,
        on_delete=models.CASCADE,
        related_name="participaciones",
    )
    docente = models.ForeignKey(
        Docente,
        on_delete=models.CASCADE,
        related_name="participaciones",
    )
    estado_asistencia = models.CharField(
        max_length=20,
        choices=EstadoAsistencia.choices,
        default=EstadoAsistencia.PENDIENTE,
    )
    horas_registradas = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["capacitacion", "docente"],
                name="participacion_unica_por_capacitacion",
            )
        ]

    def __str__(self):
        return f"{self.docente} - {self.capacitacion}"
2