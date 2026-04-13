from django.contrib import admin
from .models import Ziyaret, ZiyaretIlacKontrol # Kendi modellerini alıyor

@admin.register(Ziyaret)
class ZiyaretAdmin(admin.ModelAdmin):
    list_display = ('hasta', 'personel', 'ziyaret_tarihi', 'durum')

@admin.register(ZiyaretIlacKontrol)
class ZiyaretIlacKontrolAdmin(admin.ModelAdmin):
    list_display = ('ziyaret', 'ilac', 'hemsirenin_saydigi_adet', 'analiz_sonucu')
    
    def analiz_sonucu(self, obj):
        return obj.durum_analizi
    analiz_sonucu.short_description = "Akıllı Analiz Durumu"