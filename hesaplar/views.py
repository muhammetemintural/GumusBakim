from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from hastalar.models import Hasta
from ziyaretler.models import Ziyaret
from stok_takip.models import Malzeme
from django.utils import timezone

# 1. Ana Karşılama Sayfası
def ana_sayfa(request):
    return render(request, 'index.html')

# 2. Personel Giriş (Login) İşlemleri
def personel_giris(request):
    # Eğer butona basılmışsa (POST isteği geldiyse)
    if request.method == 'POST':
        kullanici = request.POST.get('username')
        sifre = request.POST.get('password')

        # Güvenlik Şefi: Veri tabanındaki şifreyle eşleşiyor mu kontrol et
        user = authenticate(request, username=kullanici, password=sifre)

        if user is not None:
            # Şifre doğruysa kapıyı aç ve oturum başlat
            login(request, user)
            return redirect('dashboard') # İçeri al
        else:
            # Yanlışsa ekrana kırmızı hata mesajı gönder
            messages.error(request, 'Kullanıcı adı veya şifre hatalı. Lütfen kontrol ediniz.')

    # Butona basılmadıysa sadece formu göster
    return render(request, 'login.html')

# 3. Akıllı ve Rol Tabanlı Ana Panel (Dashboard)
def dashboard(request):
    # Güvenlik: Giriş yapmamış biri direkt URL'den girmeye çalışırsa logine at
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Sisteme giren kullanıcının rolünü al
    try:
        rol = request.user.profil.rol
    except:
        # Eğer kullanıcının bir profili (rolü) yoksa, hata vermemesi için varsayılan olarak yönetici say
        rol = 'yönetici' 

    # --- 1. YÖNETİCİ (MÜDÜR) EKRANI ---
    if rol == 'yönetici':
        tum_hastalar = Hasta.objects.all().order_by('-kayit_tarihi')
        bugun = timezone.now().date()
        
        context = {
            'hastalar': tum_hastalar,
            'toplam_hasta': tum_hastalar.count(),
            'bugunku_ziyaretler': Ziyaret.objects.filter(ziyaret_tarihi__date=bugun).count(),
            'kritik_stok': Malzeme.objects.filter(stok_miktari__lt=10).count()
        }
        return render(request, 'dashboard_yonetici.html', context)

    # --- 2. HEMŞİRE (SAHA PERSONELİ) EKRANI ---
    elif rol == 'hemşire':
        bugun = timezone.now().date()
        # Sadece bu hemşireye atanmış ve BUGÜN yapılacak ziyaretleri çek
        benim_ziyaretlerim = Ziyaret.objects.filter(personel=request.user, ziyaret_tarihi__date=bugun).order_by('ziyaret_tarihi')
        
        context = {
            'benim_ziyaretlerim': benim_ziyaretlerim,
            'kalan_ziyaret_sayisi': benim_ziyaretlerim.filter(durum='planlandi').count(),
            'tamamlanan_ziyaret_sayisi': benim_ziyaretlerim.filter(durum='tamamlandi').count(),
        }
        return render(request, 'dashboard_hemsire.html', context)

    # --- 3. DOKTOR EKRANI ---
    elif rol == 'doktor':
        # Doktor ekranını tasarlayana kadar şimdilik hastaları listelesin
        tum_hastalar = Hasta.objects.all().order_by('-kayit_tarihi')
        return render(request, 'dashboard_doktor.html', {'hastalar': tum_hastalar})

    
    
    # Eğer rol bunların hiçbiri değilse güvenliğe geri at
    return redirect('home')