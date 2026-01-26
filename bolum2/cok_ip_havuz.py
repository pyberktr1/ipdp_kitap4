# cok ip üzerinde ip havuzu kullanarak uygulama örneği
# havuz ile ip kullanimi icin kutuphane
from concurrent.futures import ThreadPoolExecutor as ip_hav_islet

# zamansal performans tespiti için gerekli kütüphane
from time import perf_counter, sleep

def gorev(ipid, bas):
    print(f"gorev {ipid} basliyor...")
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
        print(f"gorev {ipid} : gecen sure : {an - bas: 2.5f} ")
    return f" gorev {ipid} tamamlandı..."

# baslangic ani kaydediliyor
bas = perf_counter()

# iki gorev havuza atilip cagriliyor
with ip_hav_islet() as isletmen:
    ip1 = isletmen.submit(gorev, 1, perf_counter())
    ip2 = isletmen.submit(gorev, 2, perf_counter())
    # havuzdaki iplerin sonuclari sorgulaniyor
    print(ip1.result())
    print(ip2.result())    

# bitis anı kaydediliyor
bit = perf_counter()
print(f"Toplam isletme suresi: {bit - bas: 2.5f} saniye")
