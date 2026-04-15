from django import forms
from django.contrib.auth.models import User  # <--- İŞTE SİSTEMİ ÇÖKERTEN EKSİK SATIR EKLENDİ
from .models import Ziyaret

class ZiyaretForm(forms.ModelForm):
    class Meta:
        model = Ziyaret
        fields = ['ziyaret_tarihi', 'durum', 'yapilan_islemler']
        
        widgets = {
            # type: 'datetime-local' sayesinde harika bir takvim çıkacak!
            'ziyaret_tarihi': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'durum': forms.Select(attrs={'class': 'form-select'}),
            'yapilan_islemler': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Planlanan veya yapılan tıbbi işlemleri yazın...'}),
        }

class GorevPlanlaForm(forms.ModelForm):
    class Meta:
        model = Ziyaret
        fields = ['hasta', 'personel', 'ziyaret_tarihi', 'islem_tipi', 'notlar']
        
        widgets = {
            'hasta': forms.Select(attrs={'class': 'form-select'}),
            'personel': forms.Select(attrs={'class': 'form-select'}),
            'ziyaret_tarihi': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'islem_tipi': forms.Select(attrs={'class': 'form-select'}),
            'notlar': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Görevin detaylarını buraya yazın...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Formda personel seçerken sadece doktor ve hemşireler çıksın (yöneticiler çıkmasın)
        self.fields['personel'].queryset = User.objects.filter(profil__rol__in=['doktor', 'hemşire'])