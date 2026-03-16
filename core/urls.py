from django.contrib import admin
from django.urls import path
from hesaplar import views as hesaplar_views  # Hesaplar app'i
from hastalar import views as hastalar_views  # Hastalar app'i
from ziyaretler import views as ziyaretler_views  # Ziyaretler app'i
from stok_takip import views as stok_views  # Stok Takip app'i

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Hesaplar rotalarındaki "views" kelimelerini "hesaplar_views" yaptık:
    path('', hesaplar_views.ana_sayfa, name='home'),
    path('login/', hesaplar_views.personel_giris, name='login'),
    path('dashboard/', hesaplar_views.dashboard, name='dashboard'),
    
    # Hasta ekleme rotası
    path('hasta-ekle/', hastalar_views.hasta_ekle, name='hasta_ekle'),

    path('hasta/<int:id>/', hastalar_views.hasta_detay, name='hasta_detay'),

    path('hasta/<int:hasta_id>/ziyaret-planla/', ziyaretler_views.ziyaret_ekle, name='ziyaret_ekle'),
    path('ziyaret/<int:ziyaret_id>/malzeme-kullan/', stok_views.malzeme_kullan, name='malzeme_kullan'),
]