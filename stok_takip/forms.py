from django import forms
from .models import ZiyaretMalzemeKullanimi, Malzeme

# 1. Saha Personelinin Ziyarette Malzeme Düştüğü Form
class MalzemeKullanimForm(forms.ModelForm):
    class Meta:
        model = ZiyaretMalzemeKullanimi
        fields = ['malzeme', 'kullanilan_miktar']
        
        widgets = {
            'malzeme': forms.Select(attrs={'class': 'form-select'}),
            # min: 1 diyerek personelin eksi veya sıfır girmesini HTML tarafında engelliyoruz
            'kullanilan_miktar': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Kaç adet/kutu kullanıldı?'}),
        }

# 2. Yöneticinin Depoya Yeni Malzeme Eklediği Form (YENİ)
class MalzemeEkleForm(forms.ModelForm):
    class Meta:
        model = Malzeme
        fields = ['ad', 'aciklama', 'stok_miktari', 'birim']
        
        widgets = {
            'ad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: İzotonik Serum 500ml'}),
            'aciklama': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Malzeme hakkında kısa bir not...'}),
            'stok_miktari': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Başlangıç stok adedi'}),
            'birim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Adet, Kutu, Şişe, Litre'}),
        }
# stok_takip/forms.py dosyasının en altına ekle

class StokArtirForm(forms.Form):
    eklenecek_miktar = forms.IntegerField(
        min_value=1,
        label="Depoya Giren Miktar",
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Kaç adet/kutu eklendi?'})
    )