from django import forms
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