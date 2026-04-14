from django.db import models
from django.contrib.auth.hashers import make_password


class Usuario(models.Model):
    """
    Modelo para almacenar los registros de usuarios con alergias.
    """
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    ciudad = models.CharField(max_length=100)
    alergias = models.JSONField(default=list)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    
    created_at = models.DateTimeField(auto_now_add=True)
    google_sheet_synced = models.BooleanField(default=False)
    
    """ configuracion """
    class Meta:
        db_table = 'usuarios'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    """ Return data as string value """ 
    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.email})"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"
    
    @property
    def nivel_riesgo(self):
        alergias_altas = ['polen', 'gramíneas', 'olivo']
        if any(a in self.alergias for a in alergias_altas):
            return "Alto"
        elif self.alergias:
            return "Moderado"
        return "Bajo"
    
    @property
    def alergenos_principales(self):
        return ", ".join(self.alergias) if self.alergias else "Ninguna"