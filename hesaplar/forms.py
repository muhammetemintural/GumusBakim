from django import forms
from django.contrib.auth.models import User
from .models import Profil

class PersonelKayitForm(forms.ModelForm):
    # Kullanıcı bilgileri
    username = forms.CharField(label="Kullanıcı Adı / Sicil No", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Geçici Şifre", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Ad", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Soyad", widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Profil bilgileri (Rol seçimi buradan yapılacak)
    rol = forms.ChoiceField(label="Sistem Rolü", choices=Profil.ROL_SECENEKLERI, widget=forms.Select(attrs={'class': 'form-select'}))
    telefon = forms.CharField(label="Telefon", required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Şifreyi şifrele
        if commit:
            user.save()
            # User oluştuktan sonra Profilini de oluştur/güncelle
            Profil.objects.update_or_create(
                user=user,
                defaults={
                    'rol': self.cleaned_data['rol'],
                    'telefon': self.cleaned_data['telefon']
                }
            )
        return user