from django.db import models
from django.utils import timezone

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

class HastaIlaci(models.Model):
    hasta = models.ForeignKey(Hasta, on_delete=models.CASCADE, related_name='ilaclar', verbose_name="Hasta")
    ilac_adi = models.CharField(max_length=100, verbose_name="İlaç Adı (Örn: Parol 500mg)")
    kutu_ici_adet = models.IntegerField(verbose_name="Kutudaki Toplam Hap Sayısı")
    gunluk_kullanim_miktari = models.IntegerField(verbose_name="Günde Kaç Adet İçiyor?")
    kutu_acilis_tarihi = models.DateField(default=timezone.now, verbose_name="Kutuyu Açtığı Tarih")
    aktif_mi = models.BooleanField(default=True, verbose_name="Kullanıma Devam Ediyor mu?")

    def __str__(self):
        return f"{self.ilac_adi} - {self.hasta.ad} {self.hasta.soyad}"

    class Meta:
        verbose_name = "Hasta İlacı"
        verbose_name_plural = "Hasta İlaçları"

    # SİSTEMİN MATEMATİKSEL BEYNİ BURASI:
    @property
    def beklenen_kalan(self):
        # Bugünün tarihi ile kutunun açıldığı tarih arasındaki gün farkını bul
        gecen_gun = (timezone.now().date() - self.kutu_acilis_tarihi).days
        
        # Kaç tane içmiş olması gerektiğini hesapla
        kullanilmasi_gereken = gecen_gun * self.gunluk_kullanim_miktari
        
        # Kutudaki toplam haptan, içilmesi gerekeni çıkar
        kalan = self.kutu_ici_adet - kullanilmasi_gereken
        
        # Eğer kalan 0'dan küçükse (kutu bitmişse) 0 göster
        return max(kalan, 0)