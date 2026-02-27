from django.db import models
from ziyaretler.models import Ziyaret

class Malzeme(models.Model):
    ad = models.CharField(max_length=100, verbose_name="Malzeme Adi")
    aciklama = models.TextField(blank=True, null=True, verbose_name="Açiklama")
    stok_miktari = models.PositiveIntegerField(default=0, verbose_name="Stok Miktari")
    birim = models.CharField(max_length=20, verbose_name="Birim (Adet, Kutu, Litre vb.)")

    def __str__(self):
        return f"{self.ad} - Kalan: {self.stok_miktari} {self.birim}"

    class Meta:
        verbose_name = "Malzeme"
        verbose_name_plural = "Malzemeler"

class ZiyaretMalzemeKullanimi(models.Model):
    ziyaret = models.ForeignKey(Ziyaret, on_delete=models.CASCADE, verbose_name="İlgili Ziyaret")
    malzeme = models.ForeignKey(Malzeme, on_delete=models.PROTECT, verbose_name="Kullanılan Malzeme")
    kullanilan_miktar = models.PositiveIntegerField(verbose_name="Kullanılan Miktar")

    def __str__(self):
        return f"{self.ziyaret.hasta.ad} ziyareti -> {self.malzeme.ad} ({self.kullanilan_miktar} {self.malzeme.birim})"

    class Meta:
        verbose_name = "Kullanılan Malzeme"
        verbose_name_plural = "Kullanılan Malzemeler"