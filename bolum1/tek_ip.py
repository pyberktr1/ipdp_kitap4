# tek ip üzerinde uygulama örneği
# zamansal performans tespiti için gerekli kütüphane
from time import perf_counter, sleep

def gorev(id, bas):
    print(f"gorev {id} basliyor...")
    # gorev burada gerceklesiyor
    for _ in range(10):
        # I/O gecikmesini simule eden kısım
        # I/O islemleri esnasında islemcinin 
        # bosta bekledigi uzun gecikmeler olur
        # I/O islemlerine ornek: web sorgulamaları, 
        # disk islemleri v.s.
        sleep(0.1)#saniye gecikme
        # bu bolumde sorgulamanın ne kadar surdugu hesaplanmakta
        an = perf_counter()
        print(f"gorev {id} : gecen sure : {an - bas: 2.3f} ")
    print(f" gorev {id} tamamlandı...")

# baslangic ani kaydediliyor
bas = perf_counter()

# iki gorev sırayla cagriliyor
gorev(1, perf_counter())
gorev(2, perf_counter())

# bitis anı kaydediliyor
bit = perf_counter()
print(f"Toplam isletme suresi: {bit - bas: 2.3f} saniye")
