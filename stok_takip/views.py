from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Malzeme, ZiyaretMalzemeKullanimi
from .forms import MalzemeKullanimForm
from ziyaretler.models import Ziyaret

def malzeme_kullan(request, ziyaret_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    # İşlem yapılacak ziyareti veri tabanından bul
    ziyaret = get_object_or_404(Ziyaret, id=ziyaret_id)
    
    if request.method == 'POST':
        form = MalzemeKullanimForm(request.POST)
        if form.is_valid():
            kullanim = form.save(commit=False)
            kullanim.ziyaret = ziyaret # Ziyareti otomatik ata
            
            malzeme = kullanim.malzeme
            miktar = kullanim.kullanilan_miktar
            
            # STOK KONTROLÜ VE DÜŞME İŞLEMİ
            if malzeme.stok_miktari >= miktar:
                # Stok yeterliyse miktarı düş ve kaydet
                malzeme.stok_miktari -= miktar
                malzeme.save() # Malzeme deposunu güncelle
                kullanim.save() # Kullanım kaydını oluştur
                
                messages.success(request, f"{miktar} {malzeme.birim} {malzeme.ad} başarıyla kaydedildi ve stoktan düşüldü.")
                return redirect('hasta_detay', id=ziyaret.hasta.id)
            else:
                # Stok yetersizse hata ver
                messages.error(request, f"HATA: Yetersiz stok! Depoda sadece {malzeme.stok_miktari} {malzeme.birim} {malzeme.ad} kaldı.")
    else:
        form = MalzemeKullanimForm()
        
    return render(request, 'malzeme_kullan.html', {'form': form, 'ziyaret': ziyaret})