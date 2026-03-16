from django import forms
from .models import ZiyaretMalzemeKullanimi

class MalzemeKullanimForm(forms.ModelForm):
    class Meta:
        model = ZiyaretMalzemeKullanimi
        fields = ['malzeme', 'kullanilan_miktar']
        
        widgets = {
            'malzeme': forms.Select(attrs={'class': 'form-select'}),
            # min: 1 diyerek personelin eksi veya sıfır girmesini HTML tarafında engelliyoruz
            'kullanilan_miktar': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Kaç adet/kutu kullanıldı?'}),
        }