# cok ip uzerinde uygulama ornegi 2a
# for döngüleri ile çoklu ip yönetimi ve iplerde tıkanma (blocking) olayı
# zamansal performans tespiti icin gerekli kutuphane
from time import perf_counter, sleep
# ip tanımlamaları icin gerekli kutuphane
from threading import Thread

def gorev(id, bas):
    print(f"gorev {id} basliyor...\n", end="")
    # gorev burada gerceklesiyor
    for _ in range(2):
        # I/O gecikmesini simule eden kısım
        # I/O islemleri esnasında islemcinin 
        # bosta bekledigi uzun gecikmeler olur
        # I/O islemlerine ornek: web sorgulamaları, 
        # disk islemleri v.s.
        sleep(0.1)
        # bu bolumde sorgulamanın ne kadar surdugu hesaplanmakta
        an = perf_counter()
        print(f"gorev {id} : gecen sure : {an - bas: 2.3f} \n", end="")
    # burada 3 numaralı gorev tikaniyor
    # tıkanmalar islemci zamanından caldigi icin 
    # istenmez. Bir ipi beklemeye almak zorunlu ise 
    # sleep() metodu ile uyutma yapılmalıdır
    while (id == 3):
        pass
        
    print(f" gorev {id} tamamlandı...\n", end="")

# baslangic ani kaydediliyor
bas = perf_counter()

# her bir gorev icin 5 adet ayri yeni ip olusturuluyor ve baslatiliyor
ipler = []
for i in range(1,6):
    ipler.append(Thread(target = gorev, args = (i, perf_counter(),)))
    ipler[i-1].start()

# iplerdeki gorevlerin tamamlanmasını bekleyelim
for ip in ipler:
    ip.join()

# bitis anı kaydediliyor
bit = perf_counter()
print(f"Toplam isletme suresi: {bit - bas: 2.3f} saniye\n", end="")
