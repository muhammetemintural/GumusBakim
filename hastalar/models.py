from django.db import models

class Hasta(models.Model):
    tc_kimlik_no = models.CharField(max_length=11, unique=True, verbose_name="TC Kimlik No")
    ad = models.CharField(max_length=50, verbose_name="Ad")
    soyad = models.CharField(max_length=50, verbose_name="Soyad")
    dogum_tarihi = models.DateField(verbose_name="Doğum Tarihi")
    telefon = models.CharField(max_length=15, verbose_name="Telefon Numarası")
    adres = models.TextField(verbose_name="Açık Adres")
    kan_grubu = models.CharField(max_length=10, blank=True, null=True,verbose_name="Kan Grubu")
    kronik_hastaliklar = models.TextField(blank=True, null=True, verbose_name="Kronik Hastalıklar")
    alerjiler = models.TextField(blank=True, null=True, verbose_name="Alerjiler")
    kayit_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    def __str__(self):
        return f"{self.ad} {self.soyad} - {self.tc_kimlik_no}"
    
    class Meta:
        verbose_name = "Hasta"
        verbose_name_plural = "Hastalar"


