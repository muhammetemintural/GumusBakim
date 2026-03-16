from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Ziyaret
from .forms import ZiyaretForm
from hastalar.models import Hasta

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
            
            messages.success(request, f"{hasta.ad} {hasta.soyad} için yeni ziyaret planlandı.")
            return redirect('hasta_detay', id=hasta.id) # Hastanın sayfasına geri dön
    else:
        form = ZiyaretForm()
        
    return render(request, 'ziyaret_ekle.html', {'form': form, 'hasta': hasta})