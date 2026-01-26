# Bu ornek zamanlayici kullanimini gosterir 
# zamanlayicilar ipler uzerinden calisir
# bir proses icinde zamanlayici kullanilabilir
# ancak bir prosesin kendisi zamanlayici olamaz

# zamanlayici kutuphanesi
import time
# ip kutuphanesi
from threading import Thread as ip
from threading import Timer, Event

# zamanlayici fonksiyonu
def zaman():
    # kapatma sinyali aktifse gorevi iptal et
    if not kapat.is_set():
        saniye[0] = saniye[0] + artim
        Timer(artim, zaman).start()
    else:
        print("zamanlayici kapatildi!")
        
# monitor hayalet ipi
def monitor():
    while not kapat.is_set():
        print(f"\rsaat(timer):{saniye[0]: 2.3f} saat(ana):{saniye[1]: 2.3f}",
                end="")
        # tazeleme hizi gecikme yokken maksimumdur, 
        # bu durumda işlemci asiri yorulur
        # 0.05 saniye ustu tazeleme araligi daha uygundur
        #time.sleep(0.1)# tazeleme gecikmesi

# ana program bolumu
if __name__ == "__main__":
    
    # Global veriyapisi
    saniye = [0.0]*2
    # gosterge cozunurlugu
    artim  = 0.01# saniye
    # bitis ani
    bitis  = 5.0# saniye
    # kapatma olayi
    kapat = Event()

    print("SAAT BASLATILDI!")

    # monitor hayalet ipi
    ip(target=monitor, daemon=True).start()
    
    # baslangic anini kaydet
    bas = time.perf_counter()
    
    # zamanlayiciyi baslat
    zaman()
    
    # ana zamanlayici fonksiyonu
    while round(saniye[1], 5)<bitis:
        time.sleep(artim)
        saniye[1] = saniye[1] + artim
    
    # zamanlayici bitis kaydet
    s0 = saniye[0]
    
    # bitis suresini kaydet
    bit = time.perf_counter() - bas

    # tum sistemi kapat, 
    # hemen kapanmadigi icin zamanlayicinin monitordeki
    # gostergesi asil bitis degerinden fazla olabilir
    time.sleep(0.1)# ana saat degerini yakalamak icin gerekli gecikme
    kapat.set()

    print("\nBaslangictan bitise kadar gecen sure     :",
        f"{bit: 2.3f} saniye")
    print(f"Zamanlayici ve ana saat arasindaki fark  :",
        f"{s0 - saniye[1]: 2.3f} saniye")
    print(f"Gercek zaman ve ana saat arasindaki fark :",
        f"{bit - saniye[1]: 2.3f} saniye")
    
