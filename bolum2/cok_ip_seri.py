# cok ip üzerinde ip havuzunu map() metoduyla 
# seri kullanarak uygulama örneği
# havuz ile ip kullanimi icin kutuphane
from concurrent.futures import ThreadPoolExecutor as ip_hav_islet

# zamansal performans tespiti için gerekli kütüphane
from time import perf_counter, sleep

def gorev(param):
    print(f"gorev {param[0]} basliyor...")
    # gorev burada gerceklesiyor
    for _ in range(10):
        # I/O gecikmesini simule eden kısım
        # I/O islemleri esnasında islemcinin bosta 
        # bekledigi uzun gecikmeler olur
        # I/O islemlerine ornek: web sorgulamaları, 
        # disk islemleri v.s.
        sleep(0.1)
        # bu bolumde sorgulamanın ne kadar surdugu hesaplanmakta
        an = perf_counter()
        print(f"gorev {param[0]} : gecen sure : {an - param[1]: 2.5f} ")
    return f" gorev {param[0]} tamamlandı..."

# baslangic ani kaydediliyor
bas = perf_counter()

# iki gorev havuza seri atilip cagriliyor
with ip_hav_islet() as isletmen:
    sonuclar = isletmen.map(gorev, [[1, perf_counter()], [2, perf_counter()]])
    for sonuc in sonuclar:
        print(sonuc)

# bitis anı kaydediliyor
bit = perf_counter()
print(f"Toplam isletme suresi: {bit - bas: 2.5f} saniye")
