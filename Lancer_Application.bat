@echo off
chcp 65001 > nul
title Fransa İş ^& Kariyer Rehberi - Uygulama Sunucusu
color 0B

echo ===============================================================================
echo        🇹🇷 FRANSA İŞ ^& KARİYER REHBERİ (TR ⇄ FR BILATERAL HUB) 🇫🇷
echo ===============================================================================
echo.
echo  [i] Sunucu ve Uygulama Hazırlanıyor... / Lancement de l'application...
echo.

:: Vérification de la présence de Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [HATA / ERREUR] Python bulunamadi !
    echo Lutfen Python 3'un kurulu ve PATH'e ekli oldugundan emin olun.
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo  [✓] Python tespit edildi.
echo  [✓] Yerel sunucu başlatılıyor (http://localhost:8080)...
echo  [✓] Varsayılan internet tarayıcınız otomatik olarak açılacaktır.
echo.
echo -------------------------------------------------------------------------------
echo  💡 KULLANIM İPUCU:
echo  - Sayfa açıldığında sağ üstteki 'Uygulamayı Yükle' veya 'Şimdi Yenile' butonunu
echo    kullanabilirsiniz.
echo  - Arka plandaki otomatik yenileme (her 12 saatte bir) devrededir.
echo  - Çıkmak için bu pencereyi kapatmanız yeterlidir.
echo -------------------------------------------------------------------------------
echo.

python app_server.py --port 8080 --auto-refresh-hours 12

if %errorlevel% neq 0 (
    echo.
    echo Sunucu durduruldu veya bir hata olustu.
    pause
)
