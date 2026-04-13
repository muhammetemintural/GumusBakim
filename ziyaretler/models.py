from django.db import models
from hastalar.models import Hasta
from django.contrib.auth.models import User
from hastalar.models import HastaIlaci

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
class ZiyaretIlacKontrol(models.Model):
    ziyaret = models.ForeignKey(Ziyaret, on_delete=models.CASCADE, related_name='ilac_kontrolleri')
    ilac = models.ForeignKey(HastaIlaci, on_delete=models.CASCADE, verbose_name="Kontrol Edilen İlaç")
    hemsirenin_saydigi_adet = models.IntegerField(verbose_name="Kutuda Kalan Sayı")
    
    def __str__(self):
        return f"{self.ziyaret.hasta.ad} - {self.ilac.ilac_adi} Kontrolü"

    class Meta:
        verbose_name = "İlaç Kontrolü"
        verbose_name_plural = "İlaç Kontrolleri"

    # ÇAPRAZ DOĞRULAMA ALGORİTMASI BURASI:
    @property
    def durum_analizi(self):
        # Hemşirenin saydığı sayıdan, sistemin beklediği sayıyı çıkar
        fark = self.hemsirenin_saydigi_adet - self.ilac.beklenen_kalan
        
        if fark == 0:
            return "Kusursuz Uyum (Düzenli İçiyor)"
        elif fark > 0:
            return f"Düzensiz! Kutu gereğinden dolu. {fark} adet eksik içmiş."
        else:
            return f"Riskli! Kutu gereğinden boş. {abs(fark)} adet FAZLA içmiş."
