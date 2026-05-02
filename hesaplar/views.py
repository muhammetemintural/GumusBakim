from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q, Count

# Diğer Uygulama Modelleri
from hastalar.models import Hasta, HastaIlac 
from ziyaretler.models import Ziyaret
from stok_takip.models import Malzeme

# Kendi Modelleri ve Formları
from .models import Profil, Mesaj
from .forms import PersonelKayitForm

# 1. Ana Karşılama Sayfası
def ana_sayfa(request):
    return render(request, 'index.html')

# 2. Personel Giriş İşlemleri
def personel_giris(request):
    if request.method == 'POST':
        kullanici = request.POST.get('username')
        sifre = request.POST.get('password')
        user = authenticate(request, username=kullanici, password=sifre)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    return render(request, 'login.html')

# 3. Akıllı ve Dinamik Ana Panel (Dashboard)
@login_required
def dashboard(request):
    try:
        rol = request.user.profil.rol
    except:
        rol = 'yönetici' 

    yeni_mesajlar_sayisi = Mesaj.objects.filter(alici=request.user, okundu_mu=False).count()
    simdi = timezone.now()
    bugun = simdi.date()

    if rol == 'yönetici':
        tum_hastalar = Hasta.objects.all().order_by('-kayit_tarihi')
        son_ziyaretler = Ziyaret.objects.all().order_by('-ziyaret_tarihi')[:10]
        kritik_stok_listesi = Malzeme.objects.filter(stok_miktari__lt=10)
        son_mesajlar = Mesaj.objects.all().order_by('-tarih')[:5]

        personeller = User.objects.exclude(is_superuser=True).select_related('profil')
        for p in personeller:
            p.bugunku_is_sayisi = Ziyaret.objects.filter(personel=p, ziyaret_tarihi__date=bugun).count()
            p.tamamlanan_is_sayisi = Ziyaret.objects.filter(personel=p, ziyaret_tarihi__date=bugun, durum='tamamlandi').count()
        
        context = {
            'hastalar': tum_hastalar,
            'son_ziyaretler': son_ziyaretler,
            'toplam_hasta': tum_hastalar.count(),
            'bugunku_ziyaretler': Ziyaret.objects.filter(personel=request.user, ziyaret_tarihi__date=bugun).count(),
            'kritik_stok_sayisi': kritik_stok_listesi.count(),
            'kritik_stoklar': kritik_stok_listesi,
            'personeller': personeller,
            'yeni_mesaj_sayisi': yeni_mesajlar_sayisi,
            'son_mesajlar': son_mesajlar,
        }
        return render(request, 'dashboard_yonetici.html', context)

    elif rol == 'hemşire':
        saat = simdi.hour
        if saat < 8: mesai_metni, mesai_renk = "Mesai Başlamadı", "secondary"
        elif 8 <= saat < 17: mesai_metni, mesai_renk = "Mesai Devam Ediyor", "info"
        elif 17 <= saat < 19: mesai_metni, mesai_renk = "Mesai Bitişi", "warning"
        else: mesai_metni, mesai_renk = "Mesai Dışı", "danger"

        benim_ziyaretlerim = Ziyaret.objects.filter(personel=request.user, ziyaret_tarihi__date=bugun).order_by('ziyaret_tarihi')
        context = {
            'benim_ziyaretlerim': benim_ziyaretlerim,
            'kalan_ziyaret_sayisi': benim_ziyaretlerim.filter(durum='planlandi').count(),
            'tamamlanan_ziyaret_sayisi': benim_ziyaretlerim.filter(durum='tamamlandi').count(),
            'yeni_mesaj_sayisi': yeni_mesajlar_sayisi,
            'mesai_durumu': mesai_metni,
            'mesai_rengi': mesai_renk,
        }
        return render(request, 'dashboard_hemsire.html', context)

    elif rol == 'doktor':
        tum_hastalar = Hasta.objects.all().order_by('-kayit_tarihi')
        return render(request, 'dashboard_doktor.html', {
            'hastalar': tum_hastalar,
            'yeni_mesaj_sayisi': yeni_mesajlar_sayisi,
        })

    return redirect('home')

# 4. İlaç Sayım Kontrolü (Kör Sayım)
@login_required
def ilac_sayim_kontrol(request, ilac_id):
    if request.user.profil.rol not in ['hemşire', 'yönetici']:
        return redirect('dashboard')

    ilac = get_object_or_404(HastaIlac, id=ilac_id)
    
    if request.method == "POST":
        fiili_stok = int(request.POST.get('fiili_stok', 0))
        sistem_beklenen = ilac.beklenen_kalan 
        
        if fiili_stok != sistem_beklenen:
            doktorlar = User.objects.filter(profil__rol='doktor')
            uyari = f"⚠️ UYUŞMAZLIK: {ilac.hasta.ad} {ilac.hasta.soyad} - {ilac.ilac_adi}. Beklenen: {sistem_beklenen}, Sayılan: {fiili_stok}."
            for dr in doktorlar:
                Mesaj.objects.create(gonderen=request.user, alici=dr, icerik=uyari, acil_mi=True)
            messages.error(request, "Uyuşmazlık tespit edildi! Doktora bildirildi.")
        else:
            messages.success(request, "Sayım başarılı, stoklar uyuşuyor.")
            
    return redirect('hasta_detay', id=ilac.hasta.id)

# 5. Mesajlaşma Sistemi
@login_required
def mesajlar_sayfasi(request, alici_id=None):
    personeller = User.objects.exclude(id=request.user.id).select_related('profil').annotate(
        okunmamis_mesaj_sayisi=Count(
            'gonderilen_mesajlar',
            filter=Q(gonderilen_mesajlar__alici=request.user, gonderilen_mesajlar__okundu_mu=False)
        )
    )
    
    secilen_alici = None
    mesajlar = []

    if alici_id:
        secilen_alici = get_object_or_404(User, id=alici_id)
        mesajlar = Mesaj.objects.filter(
            (Q(gonderen=request.user) & Q(alici=secilen_alici)) |
            (Q(gonderen=secilen_alici) & Q(alici=request.user))
        ).order_by('tarih')
        Mesaj.objects.filter(alici=request.user, gonderen=secilen_alici, okundu_mu=False).update(okundu_mu=True)

    if request.method == "POST":
        icerik = request.POST.get('icerik')
        acil = request.POST.get('acil_mi') == 'on'
        if alici_id and icerik:
            Mesaj.objects.create(gonderen=request.user, alici=secilen_alici, icerik=icerik, acil_mi=acil)
            return redirect('ozel_mesajlar', alici_id=alici_id)

    return render(request, 'mesajlar.html', {
        'personeller': personeller,
        'mesajlar': mesajlar,
        'secilen_alici': secilen_alici,
        'yeni_mesaj_sayisi': Mesaj.objects.filter(alici=request.user, okundu_mu=False).count()
    })

# 6. Yetki ve Personel Yönetimi (EKSİK OLANLAR)
@login_required
def yetki_guncelle(request, user_id):
    if request.user.profil.rol != 'yönetici':
        return redirect('dashboard')
        
    if request.method == 'POST':
        yeni_rol = request.POST.get('yeni_rol')
        hedef_kullanici = get_object_or_404(User, id=user_id)
        profil, created = Profil.objects.get_or_create(user=hedef_kullanici)
        profil.rol = yeni_rol
        profil.save()
        messages.success(request, f"{hedef_kullanici.username} yetkisi güncellendi.")
        
    return redirect('dashboard')

@login_required
def personel_kayit(request):
    if request.user.profil.rol != 'yönetici':
        return redirect('dashboard')

    if request.method == 'POST':
        form = PersonelKayitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Yeni personel kaydedildi.')
            return redirect('dashboard')
    else:
        form = PersonelKayitForm()
    return render(request, 'personel_kayit.html', {'form': form})

@login_required
def personel_listesi(request):
    if request.user.profil.rol != 'yönetici':
        return redirect('dashboard')
    doktorlar = User.objects.filter(profil__rol='doktor').select_related('profil')
    hemsireler = User.objects.filter(profil__rol='hemşire').select_related('profil')
    return render(request, 'personel_listesi.html', {'doktorlar': doktorlar, 'hemsireler': hemsireler})

@login_required
def personel_detay(request, id):
    if request.user.profil.rol != 'yönetici':
        return redirect('dashboard')
    secilen_personel = get_object_or_404(User, id=id)
    gecmis = Ziyaret.objects.filter(personel=secilen_personel, durum='tamamlandi').order_by('-ziyaret_tarihi')
    gelecek = Ziyaret.objects.filter(personel=secilen_personel, durum='planlandi').order_by('ziyaret_tarihi')
    return render(request, 'personel_detay.html', {'personel': secilen_personel, 'gecmis_gorevler': gecmis, 'gelecek_gorevler': gelecek})

# 7. Ziyaret ve Reçete İşlemleri
@login_required
def ziyaret_tamamla(request, ziyaret_id):
    ziyaret = get_object_or_404(Ziyaret, id=ziyaret_id, personel=request.user)
    ziyaret.durum = 'tamamlandi'
    ziyaret.save()
    messages.success(request, f"{ziyaret.hasta.ad} {ziyaret.hasta.soyad} ziyareti tamamlandı.")
    return redirect('dashboard')

@login_required
def toplu_recete_view(request):
    return render(request, 'toplu_recete.html')

# 8. Mesaj İşlemleri (Silme ve Düzenleme)
@login_required
def mesaj_sil(request, mesaj_id):
    mesaj = get_object_or_404(Mesaj, id=mesaj_id, gonderen=request.user)
    al_id = mesaj.alici.id
    mesaj.delete()
    return redirect('ozel_mesajlar', alici_id=al_id)

@login_required
def mesaj_duzenle(request, mesaj_id):
    mesaj = get_object_or_404(Mesaj, id=mesaj_id, gonderen=request.user)
    if request.method == "POST":
        yeni_icerik = request.POST.get('icerik')
        if yeni_icerik:
            mesaj.icerik = yeni_icerik
            mesaj.save()
    return redirect('ozel_mesajlar', alici_id=mesaj.alici.id)