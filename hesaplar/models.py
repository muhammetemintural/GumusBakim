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
class Mesaj(models.Model):
    gonderen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gonderilen_mesajlar')
    alici = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alinan_mesajlar')
    icerik = models.TextField(verbose_name="Mesaj İçeriği")
    tarih = models.DateTimeField(auto_now_add=True)
    okundu_mu = models.BooleanField(default=False)
    acil_mi = models.BooleanField(default=False, verbose_name="Acil Durum Mesajı mı?")

    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesajlar"
        ordering = ['-tarih']

    def __str__(self):
        return f"{self.gonderen} -> {self.alici}: {self.icerik[:20]}"