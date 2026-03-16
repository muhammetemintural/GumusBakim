from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

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

# 3. İçerisi (Giriş yaptıktan sonra açılacak olan ana ekran)
def dashboard(request):
    return render(request, 'dashboard.html')