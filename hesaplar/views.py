from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from hastalar.models import Hasta
from ziyaretler.models import Ziyaret
from stok_takip.models import Malzeme
from django.utils import timezone
from django.contrib.auth.models import User # PERSONEL İÇİN EKLENDİ
from .models import Profil
from .forms import PersonelKayitForm


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
        
        # Master Control İçin Ekstra Veriler:
        son_ziyaretler = Ziyaret.objects.all().order_by('-ziyaret_tarihi')[:10] # Son 10 işlem
        kritik_stok_listesi = Malzeme.objects.filter(stok_miktari__lt=10) # Sadece sayı değil, liste
        
        context = {
            'hastalar': tum_hastalar,
            'son_ziyaretler': son_ziyaretler,
            'toplam_hasta': tum_hastalar.count(),
            'bugunku_ziyaretler': Ziyaret.objects.filter(ziyaret_tarihi__date=bugun).count(),
            'kritik_stok_sayisi': kritik_stok_listesi.count(),
            'kritik_stoklar': kritik_stok_listesi,
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

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        rol = request.user.profil.rol
    except:
        rol = 'yönetici' 

    # --- 1. YÖNETİCİ (MÜDÜR) EKRANI ---
    if rol == 'yönetici':
        tum_hastalar = Hasta.objects.all().order_by('-kayit_tarihi')
        bugun = timezone.now().date()
        
        son_ziyaretler = Ziyaret.objects.all().order_by('-ziyaret_tarihi')[:10]
        kritik_stok_listesi = Malzeme.objects.filter(stok_miktari__lt=10)
        
        # YENİ: Personel Listesi ve Günlük Performans Analizi
        personeller = User.objects.exclude(is_superuser=True).select_related('profil')
        for p in personeller:
            p.bugunku_is_sayisi = Ziyaret.objects.filter(personel=p, ziyaret_tarihi__date=bugun).count()
            p.tamamlanan_is_sayisi = Ziyaret.objects.filter(personel=p, ziyaret_tarihi__date=bugun, durum='tamamlandi').count()
        
        context = {
            'hastalar': tum_hastalar,
            'son_ziyaretler': son_ziyaretler,
            'toplam_hasta': tum_hastalar.count(),
            'bugunku_ziyaretler': Ziyaret.objects.filter(ziyaret_tarihi__date=bugun).count(),
            'kritik_stok_sayisi': kritik_stok_listesi.count(),
            'kritik_stoklar': kritik_stok_listesi,
            'personeller': personeller, # Sisteme personelleri gönderiyoruz
        }
        return render(request, 'dashboard_yonetici.html', context)

    # --- Diğer roller (hemşire, doktor) aynen kalıyor ---
    elif rol == 'hemşire':
        bugun = timezone.now().date()
        benim_ziyaretlerim = Ziyaret.objects.filter(personel=request.user, ziyaret_tarihi__date=bugun).order_by('ziyaret_tarihi')
        context = {
            'benim_ziyaretlerim': benim_ziyaretlerim,
            'kalan_ziyaret_sayisi': benim_ziyaretlerim.filter(durum='planlandi').count(),
            'tamamlanan_ziyaret_sayisi': benim_ziyaretlerim.filter(durum='tamamlandi').count(),
        }
        return render(request, 'dashboard_hemsire.html', context)

    elif rol == 'doktor':
        tum_hastalar = Hasta.objects.all().order_by('-kayit_tarihi')
        return render(request, 'dashboard_doktor.html', {'hastalar': tum_hastalar})

    return redirect('home')

# YENİ: 4. Yöneticinin Personel Yetkisini Değiştirme Fonksiyonu
def yetki_guncelle(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        yeni_rol = request.POST.get('yeni_rol')
        hedef_kullanici = get_object_or_404(User, id=user_id)
        
        # Personelin profili yoksa oluştur, varsa getir
        profil, created = Profil.objects.get_or_create(user=hedef_kullanici)
        profil.rol = yeni_rol
        profil.save()
        
        messages.success(request, f"{hedef_kullanici.username} adlı personelin yetkisi '{yeni_rol.upper()}' olarak güncellendi.")
        
    return redirect('dashboard')

def personel_kayit(request):
    if not request.user.is_authenticated or request.user.profil.rol != 'yönetici':
        messages.error(request, "Bu işlem için yetkiniz yok!")
        return redirect('dashboard')

    if request.method == 'POST':
        form = PersonelKayitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Yeni personel başarıyla kaydedildi.')
            return redirect('dashboard')
    else:
        form = PersonelKayitForm()
    
    return render(request, 'personel_kayit.html', {'form': form})

# hesaplar/views.py dosyasının en altına ekle

# 1. Personel Listeleme Sayfası (Doktorlar ve Hemşireler Ayrı)
def personel_listesi(request):
    # Sadece yöneticiler girebilir
    if not request.user.is_authenticated or request.user.profil.rol != 'yönetici':
        return redirect('dashboard')
        
    doktorlar = User.objects.filter(profil__rol='doktor').select_related('profil')
    hemsireler = User.objects.filter(profil__rol='hemşire').select_related('profil')
    
    return render(request, 'personel_listesi.html', {
        'doktorlar': doktorlar,
        'hemsireler': hemsireler
    })

# 2. Personel Detay ve Sicil Sayfası (Geçmiş ve Gelecek İşler)
def personel_detay(request, id):
    if not request.user.is_authenticated or request.user.profil.rol != 'yönetici':
        return redirect('dashboard')
        
    secilen_personel = get_object_or_404(User, id=id)
    
    # Tamamlanmış (Geçmiş) İşler
    gecmis_gorevler = Ziyaret.objects.filter(personel=secilen_personel, durum='tamamlandi').order_by('-ziyaret_tarihi')
    
    # Planlanmış (Gelecek) İşler
    gelecek_gorevler = Ziyaret.objects.filter(personel=secilen_personel, durum='planlandi').order_by('ziyaret_tarihi')
    
    context = {
        'personel': secilen_personel,
        'gecmis_gorevler': gecmis_gorevler,
        'gelecek_gorevler': gelecek_gorevler,
    }
    return render(request, 'personel_detay.html', context)