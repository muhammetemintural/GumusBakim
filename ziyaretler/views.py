from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User # EKLENDİ: Personel listesi için
from .models import Ziyaret
from .forms import ZiyaretForm, GorevPlanlaForm # EKLENDİ: Görev planlama formu için
from hastalar.models import Hasta

# 1. Hastaya Özel Bireysel Ziyaret Ekleme
def ziyaret_ekle(request, hasta_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    # Hangi hastaya ziyaret planladığımızı bul
    hasta = get_object_or_404(Hasta, id=hasta_id)
    
    if request.method == 'POST':
        form = ZiyaretForm(request.POST)
        if form.is_valid():
            # Formu kaydetmeden önce durdur
            yeni_ziyaret = form.save(commit=False) 
            yeni_ziyaret.hasta = hasta # Hastayı otomatik ata
            yeni_ziyaret.personel = request.user # Sisteme giriş yapan personeli ata
            yeni_ziyaret.save() # Şimdi veri tabanına yaz
            
            # Not: Modelinde hasta.ad_soyad kullanıyorsan burayı f"{hasta.ad_soyad} için..." şeklinde de güncelleyebilirsin.
            messages.success(request, f"{hasta.ad} {hasta.soyad} için yeni ziyaret planlandı.")
            return redirect('hasta_detay', id=hasta.id) # Hastanın sayfasına geri dön
    else:
        form = ZiyaretForm()
        
    return render(request, 'ziyaret_ekle.html', {'form': form, 'hasta': hasta})


# 2. Akıllı Operasyon ve Atama Merkezi
def atama_merkezi(request):
    # Sadece yöneticiler erişebilir
    if not request.user.is_authenticated or request.user.profil.rol != 'yönetici':
        return redirect('dashboard')

    bugun = timezone.now().date()

    # Form işlemi (POST)
    if request.method == 'POST':
        form = GorevPlanlaForm(request.POST)
        if form.is_valid():
            ziyaret = form.save(commit=False)
            ziyaret.durum = 'planlandi'
            ziyaret.save()
            messages.success(request, f"Görev başarıyla {ziyaret.personel.get_full_name()} üzerine atandı.")
            return redirect('atama_merkezi') # Aynı sayfada kal, atamaya devam et
    else:
        form = GorevPlanlaForm()

    # Sol taraftaki "Müsaitlik Paneli" için personelleri çekiyoruz
    personeller = User.objects.filter(profil__rol__in=['doktor', 'hemşire']).select_related('profil')
    
    # Her personelin bugünkü görev yükünü hesaplıyoruz
    for p in personeller:
        p.bugunku_gorev_sayisi = Ziyaret.objects.filter(personel=p, ziyaret_tarihi__date=bugun).count()

    context = {
        'form': form,
        'personeller': personeller,
        'bugun': bugun,
    }
    return render(request, 'atama_merkezi.html', context)