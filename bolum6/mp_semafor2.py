# Bu ornek semafor kullanimini gosterir daha ileri bir ornektir
# kisitli sayidaki iki kaynagin paylasimini gosterir
# bu ornekte camasir makinesinde yer bulamayan dogrudan
# bulasik makinesine gider. Orasi da doluysa belli bir
# sira gecikmesini muteakip tekrar en bastan tum makineleri
# dener

# coklu proses kutuphanesi
from multiprocessing import Process, Semaphore, Array, Event
# zamanlayici kutuphanesi
import time
# rastgele sayi kutuphanesi
import random
# ip kutuphanesi
from threading import Thread as ip

# temizlik isleri prosesi
def temizlik(no, isim, camasir, bulasik, cmak, bmak):
    # baslangic anini kaydet
    bas = time.perf_counter()
    cam_bit = 0
    bul_bit = 0
    print(f"{isim} deniyor...")
    
    # tum isler tamamlanincaya kadar devam et
    while True:
        # camasir sirasina gir
        if camasir[no]>0:# camasir yoksa bosa sira bekleme
            if cmak.acquire(block=False):
                print(f"\033[96m{isim} camasira girdi. Bos makine sayisi: ",
                      f"{cmak.get_value()}\033[00m")
                # makinede isini hallet
                time.sleep(camasir[no])
                camasir[no] = 0
                # islem tamam makineyi serbest birak
                cam_bit = time.perf_counter() - bas - bul_bit
                print(f"\033[92m{isim} camasir isini ",
                      f"{cam_bit:1.3f} saniyede tamamladi\033[00m")
                cmak.release()
                
        # bulasik sirasina gir
        if bulasik[no]>0:# bulasik yoksa bosa sira bekleme
            if bmak.acquire(block=False):
                print(f"\033[96m{isim} bulasiga girdi. Bos makine sayisi: ",
                      f"{bmak.get_value()}\033[00m")
                # makinede isini hallet
                time.sleep(bulasik[no])
                bulasik[no] = 0
                # islem tamam makineyi serbest birak
                bul_bit = time.perf_counter() - bas - cam_bit
                print(f"\033[92m{isim} bulasik isini ",
                      f"{bul_bit:1.3f} saniyede tamamladi\033[00m")
                bmak.release()
                
        # sira gecikmesi, yeniden siraya girmek gerekliyse uygulanir
        if (camasir[no] > 0) or (bulasik[no] > 0):
            time.sleep(0.1)
        else:
            print(f"{isim} tum isleri toplam {time.perf_counter() - bas:1.3f},
                    saniyede tamamladi.")
            break

# zamanlayici prosesi
def zaman(kapat):
    # zaman sayimi yapiliyor
    i = 0
    while not kapat.is_set():
        print(f"\033[95mSaniye : {i}\033[00m")
        time.sleep(1)
        i+=1

# ana program bolumu
if __name__ == "__main__":

    # Sadece 3 camasir makinesi var
    cmak = Semaphore(3)

    # Sadece 2 bulasik makinesi var
    bmak = Semaphore(2)

    # 10 kisi makineleri kullanacak
    isimler = ["Salih ", "Mehmet", "Ayse  ", "Sevim ", "Nuri  ",
               "Veli  ", "Hayri ", "Vildan", "Sinem ", "Sami  "]
    
    # camasir ve bulasiklar ayarlaniyor
    camasir = Array("f", len(isimler))
    bulasik = Array("f", len(isimler))
    for i in range(len(isimler)):
        camasir[i] = 5#(random.uniform(2,5))
        bulasik[i] = 5#(random.uniform(1,3))

    # zamanlayici ipi ve durdurma olayi
    kapat = Event()
    z_ip  = ip(target=zaman, args=(kapat,))
    z_ip.start()
    
    # her bir kisi icin bir proses olusturuyor ve baslatiyoruz
    pler  = []
    for i in range(len(isimler)):
        p = Process(target=temizlik, args=(i, isimler[i], camasir, 
                     bulasik, cmak, bmak, ))
        pler.append(p)
        p.start()
        
    # proseslerin tamamlanmasi bekleniyor    
    for p in pler:
        p.join()
    
    # zamanlayiciyi durdur 
    kapat.set()
    z_ip.join()
        
    print("\nBos makine sayisi:",
          f"\nC.mak:{cmak.get_value()} :: B.mak:{bmak.get_value()}")
    print("Herkes isini tamamladi!")
    
