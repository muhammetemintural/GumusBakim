from django.contrib import admin
from .models import Hasta, HastaIlac  # DÜZELTİLDİ: HastaIlaci yerine HastaIlac yapıldı.

@admin.register(Hasta)
class HastaAdmin(admin.ModelAdmin):
    list_display = ('ad', 'soyad', 'tc_kimlik_no', 'telefon', 'kan_grubu')
    search_fields = ('ad', 'soyad', 'tc_kimlik_no')

@admin.register(HastaIlac)
class HastaIlacAdmin(admin.ModelAdmin):
    list_display = ('ilac_adi', 'hasta', 'gunluk_kullanim_miktari', 'kutu_acilis_tarihi', 'beklenen_kalan_goster')
    
    def beklenen_kalan_goster(self, obj):
        # Property'den gelen veriyi admin panelinde "Adet" birimiyle gösteriyoruz.
        return f"{obj.beklenen_kalan} Adet"
    
    beklenen_kalan_goster.short_description = "Sistemin Beklediği Kalan"