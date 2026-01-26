# Bu ornek kilit kullanan guvenli bir ip sinifinin
# nasil yazilacagini gosterir

# ip kutuphanesi (kilit nesnesi ile birlikte)
from threading import Thread, Lock
# zamanlayici kutuphanesi
from time import perf_counter, sleep

# ortak hafiza alani
mesaj = []
sayac = 0

# gunce ipinin tazelenme suresi (saniye)
sure = 1

class iplik:
    def __init__(self):
        # global degiskenler
        self.mesaj = []
        self.sayac = 0
        self.kilit = Lock()

    def islem(self, ipid):
        # lokal degisken tanimlaniyor
        durum = 0
    
        # islem 100 kere tekrarlaniyor
        for i in range(100):
            durum = durum + ipid
            sleep(0.1)
        
            # kritik bolge        
            with self.kilit:
                # kritik (hassas) bolge
                # bu kisim sadece kilit iznine sahip olan
                # ipte isletilir
        
                # durum mesaji uretiliyor ve mesaja atiliyor
                self.mesaj.append(f"{ipid} gorevinde durum ilerlemesi "
                                  f"{durum} asamasinda")
    
    def gunce(self, sure):
        # guncelleme sayisi
        taze = 0
        # sonsuz dongude mesajlar ekrana dokuluyor
        while True:
            # gunluk fonksiyonun guncellenme sikligi
            sleep(sure)
            taze+=1
            print(f"\n{taze}. tazeleme")
        
            # mesaj icin kilit talep ediliyor
            with self.kilit:
                # birikmis tum mesajlar ekrana yazdiriliyor
                for i in range(len(self.mesaj)):
                    self.sayac = self.sayac + 1
                    print(self.mesaj[i])
        
                # mesaj kutusu bosaltiliyor
                self.mesaj = []

# ana program bolumu
# bir iplik nesnesi olusturuluyor
iplikci = iplik()

# baslangic kaydediliyor
bas = perf_counter()

# ipler olusturuluyor ve baslatiliyor
ipler = []
for i in range(1,11):
    ip = Thread(target=iplikci.islem, args=(i,))
    ip.start()
    ipler.append(ip)

# gunluk ipi olusturuluyor ve baslatiliyor
# sonsuz dongude calistigi icin bu ipimiz
# ana programin bitmesiyle birlikte sonlanacak
# hayalet tipte olmasi sarttir
ip = Thread(target=iplikci.gunce, args=(sure,), daemon=True)
ip.start()

# iplerin tamamlanmasi bekleniyor
# gunluk ipi olan hayalet tipteki "gunce" ipinin
# sonlanmasini beklemek dogru olmaz
# o yuzden gunce icin bekleme yapmiyoruz
for ip in ipler:
    ip.join()
    
# bitis kaydediliyor
bit = perf_counter()

# gunce hayalet ipinin kuyruktaki son mesajlari da ekrana 
# dokmesi icin biraz bekliyoruz ( garanti icin tazeleme 
# suresinden biraz daha fazla)
sleep(sure*1.5)

# nihai sonuclar ekrana getiriliyor
print()
print(f"Tum islemler {bit - bas : 2.5f} saniyede tamamlandi")
print(f"Toplamda {iplikci.sayac} adet mesaj ekrana yazdirildi")
