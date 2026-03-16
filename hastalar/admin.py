from django.contrib import admin
from .models import Hasta

@admin.register(Hasta)
class HastaAdmin(admin.ModelAdmin):
    list_display = ('ad', 'soyad', 'tc_kimlik_no', 'telefon', 'kan_grubu') # Ana listede görünecek sütunlar
    search_fields = ('ad', 'soyad', 'tc_kimlik_no') # Arama çubuğu ekler