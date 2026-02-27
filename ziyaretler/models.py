from django.db import models
from hastalar.models import Hasta
from django.contrib.auth.models import User

class Ziyaret(models.Model):
    Durum_secenekleri = [
        ('planlandi', 'Planlandı'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal Edildi'),
    ]
    hasta = models.ForeignKey(Hasta, on_delete=models.CASCADE, verbose_name="Hasta")
    personel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,  verbose_name="Personel")
    ziyaret_tarihi = models.DateTimeField(verbose_name="Ziyaret Tarihi")
    yapilan_islemler = models.TextField(verbose_name="Yapılan İşlemler")
    durum = models.CharField(max_length=20, choices=Durum_secenekleri)

    def __str__(self):
        return f"{self.hasta} - {self.hasta.soyad} - {self.get_durum_display()}"
    
    class Meta:
        verbose_name = "Ziyaret"
        verbose_name_plural = "Ziyaretler"
