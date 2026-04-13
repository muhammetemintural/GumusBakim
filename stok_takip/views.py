import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils.timezone import now
from .models import Malzeme, ZiyaretMalzemeKullanimi
from .forms import MalzemeKullanimForm, MalzemeEkleForm  # MalzemeEkleForm'u forms.py'ye eklemeyi unutma
from ziyaretler.models import Ziyaret

# 1. Depo Listesi ve Kritik Stok Takibi
def stok_listesi(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    # Tüm malzemeleri alfabetik sırayla çekiyoruz
    malzemeler = Malzeme.objects.all().order_by('ad')
    
    # Stoğu 20'nin altına düşenleri "kritik" sayıyoruz
    kritik_malzemeler = Malzeme.objects.filter(stok_miktari__lt=20)
    
    context = {
        'malzemeler': malzemeler,
        'toplam_kalem': malzemeler.count(),
        'kritik_sayisi': kritik_malzemeler.count(),
    }
    return render(request, 'stok_listesi.html', context)

# 2. Saha Operasyonu: Malzeme Kullanımı ve Stoktan Düşüş
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

# 3. Raporlama: Tüm Stoğu Excel (CSV) Olarak İndir
def stok_excel_aktar(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Excel'in Türkçe karakterleri bozmaması için UTF-8 BOM ekliyoruz
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="GumusBakim_Stok_Raporu_{now().strftime("%Y%m%d")}.csv"'
    response.write('\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['Malzeme Adı', 'Açıklama', 'Birim', 'Mevcut Stok', 'Durum'])

    malzemeler = Malzeme.objects.all().order_by('ad')
    for m in malzemeler:
        durum = "Tükendi" if m.stok_miktari == 0 else ("Kritik" if m.stok_miktari < 20 else "Yeterli")
        writer.writerow([m.ad, m.aciklama, m.birim, m.stok_miktari, durum])

    return response

# 4. Envanter Yönetimi: Yeni Malzeme Tanımlama
def malzeme_ekle(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = MalzemeEkleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Yeni malzeme başarıyla depoya eklendi.')
            return redirect('stok_listesi')
    else:
        form = MalzemeEkleForm()

    return render(request, 'hasta_ekle.html', {'form': form, 'baslik': 'Yeni Malzeme Ekle'}) # Form şablonunu tekrar kullanabiliriz

# stok_takip/views.py dosyasının en altına ekle
from .forms import StokArtirForm # Formu yukarıdaki importlara eklemeyi unutma!

# 5. Hızlı Stok Ekleme (Artı Butonu)
def stok_artir(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    malzeme = get_object_or_404(Malzeme, id=id)
    
    if request.method == 'POST':
        form = StokArtirForm(request.POST)
        if form.is_valid():
            eklenen = form.cleaned_data['eklenecek_miktar']
            malzeme.stok_miktari += eklenen
            malzeme.save()
            
            messages.success(request, f"{malzeme.ad} stoğuna başarıyla {eklenen} {malzeme.birim} eklendi. Yeni Stok: {malzeme.stok_miktari}")
            return redirect('stok_listesi')
    else:
        form = StokArtirForm()
        
    return render(request, 'stok_artir.html', {'form': form, 'malzeme': malzeme})

# 6. Malzeme Bilgilerini Düzenleme (Kalem Butonu)
def malzeme_duzenle(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    malzeme = get_object_or_404(Malzeme, id=id)
    
    # instance=malzeme diyerek formun içinin mevcut verilerle dolu gelmesini sağlıyoruz
    if request.method == 'POST':
        form = MalzemeEkleForm(request.POST, instance=malzeme)
        if form.is_valid():
            form.save()
            messages.success(request, f"{malzeme.ad} bilgileri başarıyla güncellendi.")
            return redirect('stok_listesi')
    else:
        form = MalzemeEkleForm(instance=malzeme)
        
    return render(request, 'malzeme_ekle.html', {'form': form})