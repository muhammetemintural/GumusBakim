from django.contrib import admin
from django.urls import path
from hesaplar import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ana_sayfa, name='home'),
    path('login/', views.personel_giris, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]