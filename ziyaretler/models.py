from django.db import models
from hastalar.models import Hasta, HastaIlac
from django.contrib.auth.models import User

class Ziyaret(models.Model):
    ISLEM_CHOICES = (
        ('muayene', 'Genel Muayene'),
        ('pansuman', 'Pansuman / Yara Bakımı'),
        ('ilac_takip', 'İlaç Takibi & Kör Sayım'),
        ('enjeksiyon', 'Enjeksiyon / Serum'),
    )

    DURUM_SECENEKLERI = [
        ('planlandi', 'Planlandı'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal Edildi'),
    ]
    
    hasta = models.ForeignKey(Hasta, on_delete=models.CASCADE, verbose_name="Hasta")
    personel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Personel")
    ziyaret_tarihi = models.DateTimeField(verbose_name="Ziyaret Tarihi")
    
    # İşlem tipi ve notlar (Formlarla tam uyum için)
    islem_tipi = models.CharField(max_length=50, choices=ISLEM_CHOICES, default='muayene', verbose_name="İşlem Tipi")
    notlar = models.TextField(blank=True, null=True, verbose_name="Görev Notları")
    
    # Detaylı kayıt için yapılan işlemler alanı
    yapilan_islemler = models.TextField(verbose_name="Yapılan İşlemler", blank=True, null=True) 
    
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='planlandi', verbose_name="Ziyaret Durumu")

    def __str__(self):
        # Hasta modelinde ad_soyad alanı olmadığı için manuel birleştiriyoruz
        return f"{self.hasta.ad} {self.hasta.soyad} - {self.get_durum_display()}"
    
    class Meta:
        verbose_name = "Ziyaret"
        verbose_name_plural = "Ziyaretler"

# --- MÜKEMMEL ÇALIŞAN KÖR SAYIM ALGORİTMASI ---
class ZiyaretIlacKontrol(models.Model):
    ziyaret = models.ForeignKey(Ziyaret, on_delete=models.CASCADE, related_name='ilac_kontrolleri')
    ilac = models.ForeignKey(HastaIlac, on_delete=models.CASCADE, verbose_name="Kontrol Edilen İlaç")
    hemsirenin_saydigi_adet = models.IntegerField(verbose_name="Kutuda Kalan Sayı")
    
    def __str__(self):
        # Burada da isim birleştirmesi hatayı önler
        return f"{self.ziyaret.hasta.ad} {self.ziyaret.hasta.soyad} - {self.ilac.ilac_adi} Kontrolü"

    class Meta:
        verbose_name = "İlaç Kontrolü"
        verbose_name_plural = "İlaç Kontrolleri"

    @property
    def durum_analizi(self):
        """
        ÇAPRAZ DOĞRULAMA ALGORİTMASI:
        Hemşirenin saydığı sayıdan, sistemin (HastaIlac property) beklediği sayıyı çıkarır.
        """
        # HastaIlac modelindeki 'beklenen_kalan' property'sini kullanır
        fark = self.hemsirenin_saydigi_adet - self.ilac.beklenen_kalan
        
        if fark == 0:
            return "Kusursuz Uyum (Düzenli İçiyor)"
        elif fark > 0:
            return f"Düzensiz! Kutu gereğinden dolu. {fark} adet eksik içmiş."
        else:
            return f"Riskli! Kutu gereğinden boş. {abs(fark)} adet FAZLA içmiş."