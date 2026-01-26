# Bu modul web isteklerini iplere dayalı olarak
# yerine getiren bir sinifi Thread sinifindan
# turetir ve kullanima sunar
# ip kutuphanesi
from threading import Thread
# web istekleri kutuphanesi
import requests
# zamansal performans tespiti icin gerekli kutuphane
from time import perf_counter, sleep

# web sayfasi indirici sinifi
class Web(Thread):
    # ip nesnesi baslaticisi
    def __init__(self, site_ad: str, ipid: None) -> None:
        super().__init__()
        self.site_ad  = site_ad         # site adresi
        self.bas      = perf_counter()  # baslangic ani
        self.ipid     = ipid            # ip seri nosu
        self.durum    = None            # site durum
        self.sure     = None            # isletim suresi
    
    # ip isletiminden sorumlu metot
    def run(self):
        # gecikme simulasyonu icin asagidaki kod bolumunu 
        # '#' karakterini basa ekleyerek aktiflestirin
        """ 3 nolu ipi kasıtlı olarak bekletiyoruz
        if self.ipid == 3:
            sleep(3)
            #"""
        # tarayici tanimlamasi icin gerekli olan baslik stringi
        baslik = {
            "User-Agent":   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "+
                            "AppleWebKit/537.36 (KHTML, like Gecko) "+
                            "Chrome/138.0.0.0 Safari/537.36 "
        }
        # ilgili sayfaya web istegi yapiliyor
        # sonuc cevap nesnesine kaydedilir
        cevap = requests.get(self.site_ad, headers = baslik)
        # talep sonucu kayitlaniyor
        self.durum = cevap.status_code
        if  self.durum == 200: # getirme islemi basarili
            # HTML verisini dosyaya kaydediyoruz
            with open(f".\\webler\\web_{self.ipid}.htm", 'wb') as d:
                d.write(cevap.text.encode("UTF-8"))
        # bitirme suresini kaydet
        self.sure = perf_counter() - self.bas
        
    # ip nesnesi uzerinde print() komutu uygulamasi durumunda 
    # yazdırılacak katar deger bu metot tarafindan otomatik saglanir 
    def __str__(self):
        msg = f"{self.ipid} :: Site : {self.site_ad:50s} : "
        msg+= f"Durum : {self.durum} :: Süre : {self.sure: 2.5f} saniye"
        return msg
               
