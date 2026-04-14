from django.contrib import admin
from django.urls import path
from hesaplar import views as hesaplar_views
from hastalar import views as hastalar_views
from ziyaretler import views as ziyaretler_views
from stok_takip import views as stok_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', hesaplar_views.ana_sayfa, name='home'),
    path('login/', hesaplar_views.personel_giris, name='login'),
    path('dashboard/', hesaplar_views.dashboard, name='dashboard'),
    path('', hesaplar_views.ana_sayfa, name='home'),
    path('login/', hesaplar_views.personel_giris, name='login'),
    path('dashboard/', hesaplar_views.dashboard, name='dashboard'),
    path('personel-kayit/', hesaplar_views.personel_kayit, name='personel_kayit'),
    
    path('hasta-ekle/', hastalar_views.hasta_ekle, name='hasta_ekle'),
    path('hasta/<int:id>/', hastalar_views.hasta_detay, name='hasta_detay'),
    path('hasta/<int:hasta_id>/ziyaret-planla/', ziyaretler_views.ziyaret_ekle, name='ziyaret_ekle'),
    
    path('ziyaret/<int:ziyaret_id>/malzeme-kullan/', stok_views.malzeme_kullan, name='malzeme_kullan'),
    
    
    # --- YENİ EKLENEN STOK ROTALARI ---
    path('stok-depo/', stok_views.stok_listesi, name='stok_listesi'),
    path('stok-depo/ekle/', stok_views.malzeme_ekle, name='malzeme_ekle'),
    path('stok-depo/excel/', stok_views.stok_excel_aktar, name='stok_excel_aktar'),
    # core/urls.py içine eklenecek rotalar:
    path('stok-depo/artir/<int:id>/', stok_views.stok_artir, name='stok_artir'),
    path('stok-depo/duzenle/<int:id>/', stok_views.malzeme_duzenle, name='malzeme_duzenle'),
    path('yetki-guncelle/<int:user_id>/', hesaplar_views.yetki_guncelle, name='yetki_guncelle'),

    # core/urls.py içine hesaplar_views rotalarının olduğu yere ekle:
    path('personel-yonetimi/', hesaplar_views.personel_listesi, name='personel_listesi'),
    path('personel-yonetimi/<int:id>/', hesaplar_views.personel_detay, name='personel_detay'),
    
    
]