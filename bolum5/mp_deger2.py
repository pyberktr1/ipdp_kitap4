# Bu ornek paylasilmis deger kullanimini gosterir
# daha ileri bir ornektir

# coklu proses kutuphanesi
from multiprocessing import Process, Value, Lock
# zamanlayici kutuphanesi
import time
# rastgele sayi kutuphanesi
import random

# soyunma kabini prosesi
def kabin(isim, bos):
    # baslangic anini kaydet
    bas = time.perf_counter()
    
    # bos bir kabin buluncaya kadar dene
    while True:
        # bos degerine kilit atiliyor
        with bos.get_lock():
            # bos kabin var mi?
            if bos.value > 0:
                # bos kabin var
                bos.value -= 1
                print(f"\033[96m{isim} kabine girdi. Bos kabin sayisi: ",
                      f"{bos.value}\033[00m")
                break
        
        # bos kabin yok, bekle
        print(f"\033[91m{isim} bekliyor...\033[00m")
        # zaman geciyor... Biraz sonra tekrar dene
        time.sleep(1)
        print(f"\033[93m{isim} tekrar deniyor...\033[00m")

    # kabinde isini hallet
    time.sleep(2 + random.uniform(0,3))
    # islem tamam kabini serbest birak
    with bos.get_lock():
        bos.value +=1
    print(f"\033[92m{isim} isini ",
          f"{time.perf_counter() - bas :1.3f} saniyede tamamladi\033[00m")

# ana program bolumu
if __name__ == "__main__":

    # Sadece 3 kabin var
    bos = Value('i', 3)

    # 5 kisi kabini kullanacak
    isimler = ["Salih", "Mehmet", "Ayse", "Sevim", "Nuri"]

    # her bir kisi icin bir proses olusturuyor ve baslatiyoruz
    pler = []
    for isim in isimler:
        p = Process(target=kabin, args=(isim, bos, ))
        pler.append(p)
        p.start()
        
    # zaman sayimi yapiliyor
    for i in range(9):
        print(f"\033[95mSaniye : {i}\033[00m")
        time.sleep(1)
    
    # proseslerin tamamlanmasi bekleniyor    
    for p in pler:
        p.join()
        
    print(f"\nBos kabin sayisi: {bos.value}")
    print("Herkes isini tamamladi!")
    
