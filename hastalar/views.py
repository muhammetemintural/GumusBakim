from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import HastaForm
from .models import Hasta
from django.shortcuts import render, redirect, get_object_or_404
from ziyaretler.models import Ziyaret

def hasta_ekle(request):
    # Güvenlik: Sadece giriş yapmış personeller hasta ekleyebilir
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = HastaForm(request.POST)
        if form.is_valid():
            form.save() # Veri tabanına kaydet
            messages.success(request, 'Yeni hasta başarıyla sisteme kaydedildi.')
            return redirect('dashboard') # Kayıttan sonra ana panele dön
    else:
        form = HastaForm() # Sayfa ilk açıldığında boş formu göster

    return render(request, 'hasta_ekle.html', {'form': form})

def hasta_detay(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    secilen_hasta = get_object_or_404(Hasta, id=id)
    
    # YENİ EKLENEN SATIR: Bu hastaya ait ziyaretleri tarihe göre (en yeni en üstte) çek
    ziyaret_gecmisi = Ziyaret.objects.filter(hasta=secilen_hasta).order_by('-ziyaret_tarihi')
    
    # 'ziyaretler' verisini de sayfaya gönderiyoruz
    return render(request, 'hasta_detay.html', {
        'hasta': secilen_hasta, 
        'ziyaretler': ziyaret_gecmisi
    })