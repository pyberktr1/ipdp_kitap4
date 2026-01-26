# Bu ornek kilit kullanilmadigi takdirde iki ip,
# arasinda ortak bir kaynagin paylasimi esnasinda
# yasanack rekabetin sonuclarini gostermektedir

# ip kutuphanesi
from threading import Thread
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
        # sayac artiriliyor
        gecici = sayac
        gecici = gecici + 1
    
        # islem gecikmesi
        sleep(0.2)
        
        # sayac guncelleniyor
        sayac = gecici
    
        # islem sonucu ekrana yazdiriliyor
        print(f"{id} gorevinde sayac = {sayac}\n", end="")

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
