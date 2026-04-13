from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    ROL_SECENEKLERI = (
        ('doktor', 'Doktor'),
        ('hemşire', 'Hemşire'),
        ('yönetici', 'Yönetici'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    rol = models.CharField(max_length=20, choices=ROL_SECENEKLERI, default='Hemsire', verbose_name="Rol / Ünvan")
    telefon = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefon Numarası")

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profiller"
