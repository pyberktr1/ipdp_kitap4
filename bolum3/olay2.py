# bu ornek olay nesneleri araciligi ile iplerarasi
# haberlesme ile ip akisinin nasil sirali hale
# getirilecegini gosterir

# ip ve olay kutuphaneleri
from threading import Thread, Event
# zamanlayici kutuphanesi
from time import sleep, perf_counter

def gorev(bekle , tetikle: Event, ipid: int) -> None:
    # ip baslatmasini bekle
    bekle.wait()
    # ip islemleri
    print(f"ip {ipid} basladi ve beklemede...\n",end="")
    sleep(2)
    # 3 nolu gorev kasitli olarak geciktiriliyor
    if ipid == 3:
        sleep(5)
    print(f"ip {ipid} tamamlandi.")
    # siradaki ipi tetikle
    tetikle.set()

# ana program bolumu
def main() -> None:
    
    # ip sayisi tanimlaniyor
    max_ip = 5
    
    # bir dizi olay nesnesi ve ip olusturuluyor
    olaylar = []
    ipler   = []
    for i in range(max_ip):
        olaylar.append(Event())
    
    for i in range(max_ip):
        # tetikleme olayi belirleniyor
        if i < (max_ip - 1):
            k = i + 1
        else:
            k = i
        ipler.append(Thread(target=gorev, args=(olaylar[i], olaylar[k], i+1)))

    # ipler baslatiliyor
    for ip in ipler:
        ip.start()

    print("Tum gorevler basladi...")
    print()
    
    bas = perf_counter()
    
    # tum gorevler sirayla tamamlaniyor
    # ilk domino tasini devirelim
    olaylar[0].set()
    
    for ip in ipler:
        ip.join()
    
    bit = perf_counter()
    
    print("Tum gorevler bitti...")
    print(f"Gorevler {bit - bas : 2.5f} saniyede tamamlandi")
    
# ana program fonksiyonu __main__ ad alanindan cagriliyor
if __name__ == "__main__":
    main()
