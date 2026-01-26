# Bu ornek kilit kullanmak suretiyle iki ip,
# arasinda ortak bir kaynagin paylasimi esnasinda
# yasanan rekabetin olumsuz sonuclarinin nasil
# ortadan kaldirildigini gostermektedir
# bu ornekte ayrica dogru performans kriterlerini
# saglamak amaciyla gorev tasarimi yeniden duzenleniyor

# ip kutuphanesi (kilit nesnesi ile birlikte)
from threading import Thread, Lock
# zamanlayici kutuphanesi
from time import perf_counter, sleep

# ortak hafiza alani
sayac = 0

# islem ipi
def islem(id):
    # sayac degiskeni global tanimlaniyor
    global sayac
    # islem 5 kere tekrarlaniyor
    for i in range(5):
        # asil islev ortak sayacla dogrudan ilgili
        # olmadigi icin kritik bolge disina aliniyor
        # islem gecikmesi
        sleep(0.2)
        
        # kritik bolgeye giriste destur cekiyoruz
        # musaitse kilit ilgili ipe tayin edilir
        # degilse ilgili ip beklemeye alinir
        kilit.acquire()
        
        # kritik (hassas) bolge
        # bu kisim sadece kilit iznine sahip olan
        # ipte isletilir
        
        # sayac artiriliyor
        gecici = sayac
        gecici = gecici + 1
    
        # sayac guncelleniyor
        sayac = gecici
    
        # islem sonucu ekrana yazdiriliyor
        print(f"{id} gorevinde sayac = {sayac}\n", end="")
        
        # ortak kaynak "sayac" ile isimiz bitti
        # hassas bolgeden cikis gerceklestiriliyor
        # kilit diger iplerin kullanmasi icin serbest birakiliyor
        kilit.release()

# ana program bolumu
# kilit nesnesi olusturuluyor
kilit = Lock()

# baslangic kaydediliyor
bas = perf_counter()

# ipler olusturuluyor
ip1 = Thread(target=islem, args=(1,))
ip2 = Thread(target=islem, args=(2,))

# ipler baslatiliyor
ip1.start()
ip2.start()

# iplerin tamamlanmasi bekleniyor
ip1.join()
ip2.join()

# bitis kaydediliyor
bit = perf_counter()

# nihai sonuc ekrana getiriliyor
print(f"Nihai sayac = {sayac}")
print(f"Tum islemler {bit - bas : 2.5f} saniyede tamamlandi")
