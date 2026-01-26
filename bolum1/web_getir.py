# Bu program istenilen sitelere ait sayfaları indirerek diske kaydeder
# site bilgisini inidiren ve kaydeden modul
from web import Web
# zamansal performans tespiti icin gerekli kutuphane
from time import perf_counter, sleep

# web adresleri tanimlaniyor
site_adlar = [
                "http://www.sm0vpo.com/rx/tda7k-rx2.htm",
                "http://www.sm0vpo.com/rx/tba120-1.htm",
                "http://www.sm0vpo.com/rx/tda7000.htm",
                "http://www.sm0vpo.com/rx/quickrx.htm",
                "http://www.sm0vpo.com/rx/synth.htm",
                "http://www.elektormagazine.com/"
                ]

# kronometre baslatiliyor
print(f"Sayfalar getiriliyor...")    
bas = perf_counter()

# her bir site icin ayri birer ip baslatiliyor
ipler = []
i = 0 # ip seri no sayaci
for site_ad in site_adlar:
    i = i + 1
    ip = Web(site_ad, i)
    ipler.append(ip)    
    ip.start()

# iplerin tamamlanmasi bekleniyor ve
# tamamlanan iplerin sonuclari ekrana basiliyor
toplam_ip_suresi = 0
for ip in ipler:
    ip.join()
    print(ip)# ip sonucu yazdiriliyor
    # ip isletim suresi toplam sureye ekleniyor
    # bu sayac seri isletim durumunda gorulecek
    # isletim suresini verir
    toplam_ip_suresi+=ip.sure
    
print(f"Tüm islemler {perf_counter()-bas:2.5f} saniye icerisinde tamamlandi.")
print(f"Ote yandan ip sureleri toplami {toplam_ip_suresi: 2.5f} saniye oldu.")