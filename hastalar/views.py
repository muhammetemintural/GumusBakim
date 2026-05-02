from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rest_framework import generics 
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import HastaForm
from .models import Hasta, HastaIlac,IslemLog
from ziyaretler.models import Ziyaret
from django.utils import timezone


# EKSİK OLAN IMPORT BURADAYDI: ZiyaretSerializer eklendi!
from .serializers import HastaIlacSerializer, ZiyaretSerializer 


class SonZiyaretView(generics.RetrieveAPIView):
    serializer_class = ZiyaretSerializer

    def get_object(self):
        hasta_id = self.kwargs.get('hasta_id')
        return Ziyaret.objects.filter(hasta_id=hasta_id).order_by('-ziyaret_tarihi').first()


class IlacGuncelleView(generics.UpdateAPIView):
    queryset = HastaIlac.objects.all()
    serializer_class = HastaIlacSerializer


def hasta_ekle(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = HastaForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Yeni hasta başarıyla sisteme kaydedildi.')
            return redirect('dashboard') 
    else:
        form = HastaForm() 

    return render(request, 'hasta_ekle.html', {'form': form})


def hasta_detay(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    secilen_hasta = get_object_or_404(Hasta, id=id)
    ziyaretler = Ziyaret.objects.filter(hasta=secilen_hasta).order_by('-ziyaret_tarihi')
    ilaclar = secilen_hasta.ilaclar.all() 
    
    # YENİ: Hastanın tüm sistem loglarını tarihe göre en yeniden eskiye doğru çekiyoruz
    loglar = IslemLog.objects.filter(hasta=secilen_hasta).order_by('-tarih')
    
    return render(request, 'hasta_detay.html', {
        'hasta': secilen_hasta, 
        'ziyaretler': ziyaretler,
        'ilaclar': ilaclar,
        'loglar': loglar # YENİ EKLENDİ
    })


def hasta_listesi(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    tum_hastalar = Hasta.objects.all().order_by('-kayit_tarihi')
    
    context = {
        'hastalar': tum_hastalar,
        'toplam_hasta': tum_hastalar.count(),
    }
    return render(request, 'hasta_listesi.html', context)


def hasta_ilac_ekle(request, hasta_id):
    if request.method == "POST":
        hasta = get_object_or_404(Hasta, id=hasta_id)
        
        ilac_adi = request.POST.get('ilac_adi')
        doz = request.POST.get('doz')
        
        try:
            HastaIlac.objects.create(
                hasta=hasta,
                ilac_adi=ilac_adi,
                gunluk_kullanim_miktari=int(doz) if doz.isdigit() else 1,
                kutu_ici_adet=30, 
                aktif_mi=True
            )
            messages.success(request, f"{ilac_adi} reçeteye eklendi.")
        except Exception as e:
            messages.error(request, f"Hata: {e}")
            
        return redirect('hasta_detay', id=hasta.id)
    return redirect('dashboard')


@api_view(['GET'])
def api_hasta_ilaclar(request, hasta_id):
    ilaclar = HastaIlac.objects.filter(hasta_id=hasta_id)
    serializer = HastaIlacSerializer(ilaclar, many=True)
    return Response(serializer.data)

def ziyaret_ekle(request, hasta_id):
    if request.method == "POST":
        hasta = get_object_or_404(Hasta, id=hasta_id)
        
        tansiyon = request.POST.get('tansiyon', 'Belirtilmedi')
        seker = request.POST.get('seker', 'Belirtilmedi')
        gelen_not = request.POST.get('notlar', '')
        
        zengin_not = f"Tansiyon: {tansiyon} | Şeker: {seker}\nİşlem Detayı: {gelen_not}"
        
        try:
            # 1. Ziyareti Kaydet
            from ziyaretler.models import Ziyaret 
            Ziyaret.objects.create(
                hasta=hasta,
                personel=request.user,  
                durum='tamamlandi',     
                notlar=zengin_not,
                ziyaret_tarihi=timezone.now() # İŞTE VERİTABANININ İSTEDİĞİ O EKSİK PARÇA!
            )
            
            # 2. LOG KAYDINI OLUŞTUR
            IslemLog.objects.create(
                hasta=hasta,
                kullanici=request.user,
                islem_ozeti="Yeni Klinik Ziyaret Kaydı Oluşturuldu",
                detay=zengin_not
            )
            
            messages.success(request, "Ziyaret başarıyla kaydedildi ve loglandı.")
        except Exception as e:
            messages.error(request, f"Kayıt Hatası: {e}")
            print(f"!!! SİSTEM LOG HATASI !!! : {e}")
            
        return redirect('hasta_detay', id=hasta.id)
    return redirect('dashboard')