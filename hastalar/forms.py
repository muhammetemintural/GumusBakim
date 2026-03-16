from django import forms
from .models import Hasta

class HastaForm(forms.ModelForm):
    class Meta:
        model = Hasta
        # Hangi alanların formda görüneceğini seçiyoruz (Kayıt tarihini sistem otomatik atar)
        fields = ['tc_kimlik_no', 'ad', 'soyad', 'dogum_tarihi', 'telefon', 'kan_grubu', 'adres', 'kronik_hastaliklar', 'alerjiler']
        
        # Arayüzü güzelleştirmek için her kutuya Bootstrap class'ı (form-control) ekliyoruz
        widgets = {
            'tc_kimlik_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '11 Haneli TC No'}),
            'ad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hastanın Adı'}),
            'soyad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hastanın Soyadı'}),
            'dogum_tarihi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '05...'}),
            'kan_grubu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: A Rh+'}),
            'adres': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Açık Ev Adresi'}),
            'kronik_hastaliklar': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Tansiyon, Şeker vb.'}),
            'alerjiler': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'İlaç veya gıda alerjileri'}),
        }