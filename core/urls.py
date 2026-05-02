from django.contrib import admin
from django.urls import path
from hesaplar import views as hesaplar_views
from hastalar import views as hastalar_views
from ziyaretler import views as ziyaretler_views
from stok_takip import views as stok_views

urlpatterns = [
    # --- YÖNETİM PANELİ ---
    path('admin/', admin.site.urls),
    
    # --- GENEL VE PERSONEL SİSTEMİ ---
    path('', hesaplar_views.ana_sayfa, name='home'),
    path('login/', hesaplar_views.personel_giris, name='login'),
    path('dashboard/', hesaplar_views.dashboard, name='dashboard'),
    path('personel-kayit/', hesaplar_views.personel_kayit, name='personel_kayit'),
    path('yetki-guncelle/<int:user_id>/', hesaplar_views.yetki_guncelle, name='yetki_guncelle'),
    path('personel-yonetimi/', hesaplar_views.personel_listesi, name='personel_listesi'),
    path('personel-yonetimi/<int:id>/', hesaplar_views.personel_detay, name='personel_detay'),
    
    # --- HASTA VE KLİNİK İŞLEMLERİ ---
    path('hasta-ekle/', hastalar_views.hasta_ekle, name='hasta_ekle'),
    path('hasta/<int:id>/', hastalar_views.hasta_detay, name='hasta_detay'),
    path('klinik-merkezi/', hastalar_views.hasta_listesi, name='hasta_listesi'),
    path('hasta/<int:hasta_id>/ilac-ekle/', hastalar_views.hasta_ilac_ekle, name='hasta_ilac_ekle'),
    path('toplu-recete/', hesaplar_views.toplu_recete_view, name='toplu_recete'), 
    
    # --- SAHA OPERASYONLARI VE ZİYARETLER ---
    path('atama-merkezi/', ziyaretler_views.atama_merkezi, name='atama_merkezi'),
    path('hasta/<int:hasta_id>/ziyaret-planla/', ziyaretler_views.ziyaret_ekle, name='ziyaret_ekle'),
    path('ziyaret/<int:ziyaret_id>/malzeme-kullan/', stok_views.malzeme_kullan, name='malzeme_kullan'),
    
    # --- MERKEZ DEPO VE STOK TAKİBİ ---
    path('stok-depo/', stok_views.stok_listesi, name='stok_listesi'),
    path('stok-depo/ekle/', stok_views.malzeme_ekle, name='malzeme_ekle'),
    path('stok-depo/excel/', stok_views.stok_excel_aktar, name='stok_excel_aktar'),
    path('stok-depo/artir/<int:id>/', stok_views.stok_artir, name='stok_artir'),
    path('stok-depo/duzenle/<int:id>/', stok_views.malzeme_duzenle, name='malzeme_duzenle'),
    path('hasta/<int:hasta_id>/ziyaret-ekle/', hastalar_views.ziyaret_ekle, name='ziyaret_ekle'),
    
    # --- MERKEZİ İLETİŞİM (WHATSAPP MANTIĞI) ---
    path('mesajlar/', hesaplar_views.mesajlar_sayfasi, name='mesajlar'),
    path('mesajlar/<int:alici_id>/', hesaplar_views.mesajlar_sayfasi, name='ozel_mesajlar'),
    path('mesaj-sil/<int:mesaj_id>/', hesaplar_views.mesaj_sil, name='mesaj_sil'),
    path('mesaj-duzenle/<int:mesaj_id>/', hesaplar_views.mesaj_duzenle, name='mesaj_duzenle'),
    path('ziyaret-tamamla/<int:ziyaret_id>/', hesaplar_views.ziyaret_tamamla, name='ziyaret_tamamla'),
    path('ilac-kontrol/<int:ilac_id>/', hesaplar_views.ilac_sayim_kontrol, name='ilac_sayim_kontrol'),
    path('api/hasta/<int:hasta_id>/ilaclar/', hastalar_views.api_hasta_ilaclar, name='api_hasta_ilaclar'),
    path('api/ilac/<int:pk>/guncelle/', hastalar_views.IlacGuncelleView.as_view(), name='api_ilac_guncelle'),
    path('api/hasta/<int:hasta_id>/son-ziyaret/', hastalar_views.SonZiyaretView.as_view()),
]