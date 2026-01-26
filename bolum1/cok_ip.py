# cok ip uzerinde uygulama ornegi
# zamansal performans tespiti icin gerekli kutuphane
from time import perf_counter, sleep
# ip tanımlamaları icin gerekli kutuphane
from threading import Thread

def gorev(id, bas):
    print(f"gorev {id} basliyor...\n", end="")
    # gorev burada gerceklesiyor
    for _ in range(10):
        # I/O gecikmesini simule eden kısım
        # I/O islemleri esnasında islemcinin 
        # bosta bekledigi uzun gecikmeler olur
        # I/O islemlerine ornek: web sorgulamaları, 
        # disk islemleri v.s.
        sleep(0.1)
        # bu bolumde sorgulamanın ne kadar surdugu hesaplanmakta
        an = perf_counter()
        print(f"gorev {id} : gecen sure : {an - bas: 2.3f} \n", end="")
    print(f" gorev {id} tamamlandı...\n", end="")

# baslangic ani kaydediliyor
bas = perf_counter()

# her bir gorev icin birer adet ayri yeni ip olusturuluyor
ip1 = Thread(target = gorev, args = (1, perf_counter(),))
ip2 = Thread(target = gorev, args = (2, perf_counter(),))

# ipleri sirasiyla baslatalim
ip1.start()
ip2.start()

# iplerdeki gorevlerin tamamlanmasını bekleyelim
ip1.join()
ip2.join()

# bitis anı kaydediliyor
bit = perf_counter()
print(f"Toplam isletme suresi: {bit - bas: 2.3f} saniye\n", end="")
