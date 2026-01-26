# cok ip havuzu kullanarak webden resim indirme uygulamasi örnegi
# havuz ile ip kullanimi icin kutuphane
from concurrent.futures import ThreadPoolExecutor as ip_hav_islet
# webden veri indirmek icin gerekli kutuphane
import requests
# resim adlarini doğru koda donusturmek icin gerekli kutuphane
import urllib.parse

# zamanlayici kutuphanesi
import time
# isletim sistemi dosya araclari kutuphanesi
import os

# webden imaj indirme fonksiyonu
def im_indir(url):
    # tarayici tanimlamasi icin gerekli olan baslik stringi
    # dogru tarayıcı tanıtımı yapilmazsa site ilgili istege
    # cevap vermeyebilir
    baslik = {
            "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "+
                            "AppleWebKit/537.36 (KHTML, like Gecko) "+
                            "Chrome/138.0.0.0 Safari/537.36 "
        }
    # ikili resim verisi
    data = None
    # web kaynagi acilip indirme gerceklestiriliyor
    # sonuc cevap nesnesine kaydedilir
    cevap = requests.get(url, headers = baslik)
    # talep sonucu kayitlaniyor
    durum = cevap.status_code
    if durum == 200: # getirme islemi basarili
        # istek verisi content özelligine kayitlidir
        data = cevap.content
        # dosya ismi duzenleniyor
        d_ad = urllib.parse.unquote(os.path.basename(url).replace("File:",""))
        # resim verisi diske kaydediliyor
        with open(f"./resim/{d_ad}", 'wb') as im_d:
            im_d.write(data)
            print(f'{d_ad} kaydedildi...')
    else:
        print(f"\033[91mHata!: {url} :: kod={durum} \033[0m")
        # rutinden cikis gerceklesiyor
        return
        
# ana program blogu
bas = time.perf_counter()

urller = [

    "http://www.sm0vpo.com/rx/tda7k-rx2_01cct.gif",
    "http://www.sm0vpo.com/rx/tda7k-rx2e.jpg",
    "http://www.sm0vpo.com/rx/tda7k",#hatali adres!
    "http://www.sm0vpo.com/rx/tda7k-rx2b.jpg",
    "http://www.sm0vpo.com/rx/tda7k-rx2a.jpg",
    "http://www.sm0vpo.com/rx/tda7k-rx2f.jpg",
    "http://www.sm0vpo.com/rx/tda7k-rx2c.jpg",
    "http://www.sm0vpo.com/rx/tda7k-rx2d.jpg"

]
# indirici ipler havuza atilip isletiliyor 
with ip_hav_islet() as isletmen:
      isletmen.map(im_indir, urller)

bit = time.perf_counter()    

print(f"Tüm resim indirme islemleri {bit - bas : 2.5f} saniye surdu")
