# bu ornek biri uretici (on uc) biri araci (ara uc) ve digeri
# tuketici (son uc) olmak uzere uc ip arasinda kuyruklar 
# araciligi ile nasil veri paylasimi yapildigini gostermektedir

# zamanlayici kutuphanesi
from time import sleep, perf_counter
# kuyruk kutuphanesi
from queue import Queue, Full, Empty
# ip kutuphanesi
from threading import Thread, Event

# global veri yapisi
ornekleme_peryodu   = 0.1   # saniye
buf_sure            = 1     # saniye
buf_ebat            = buf_sure // ornekleme_peryodu # ornek
buf_yari_sure       = buf_sure / 2 # saniye


# uretici ipi
def uret(dur:Event, kuyruk1):
    ornek = 1
    # durdurma sinyali gelinceye kadar devam et
    while not (dur.is_set()):
        try:
            # bir ornek kuyruk1 e eklenmeye
            # calisiliyor
            kuyruk1.put(ornek, block = False)
        except Full: # kuyrugun bosalmasini bekle
            sleep(buf_yari_sure)
            continue
        else: # kuyruk1 e ekleme basarili
            # bir sonraki ornek hazirlaniyor
            ornek = ornek + 1
    
    # uretim durduruldu

# araci ipi
def ara(dur:Event, kuyruk1, kuyruk2):
    # baslangic rutini, giris kuyrugu (kuyruk1) doluncaya kadar bekle
    while not kuyruk1.full():
        sleep(ornekleme_peryodu)
    
    # durdurma sinyali gelinceye kadar devam et
    while not (dur.is_set()):
        # kuyruk2 doluncaya kadar devam et
        # kuyruk2 doldurma rutini
        try:
            # bir ornek cekilmeye calisiliyor
            ornek = kuyruk1.get(block = False) 
        except Empty: # kuyruk1 bos dolmasini bekle
            sleep(ornekleme_peryodu) 
            continue
        else: # kuyruk1 den bir ornek cekildi
            tmm = False
            while not tmm:
                # cekilen ornegi kuyruk2 ye at
                try:
                    # bir ornek kuyruk2 ye eklenmeye
                    # calisiliyor
                    kuyruk2.put(ornek, block = False)
                except Full:
                    # kuyruk2 nin bosalmasini bekle
                    sleep(buf_yari_sure)
                    continue
                else:# kuyruk2 ye ekleme tamamlandi
                    # ara islem suresi
                    sleep(ornekleme_peryodu / 10)
                    tmm = True

            # kuyruktan cekilen is tamamlandi
            kuyruk1.task_done()
    
    # calma sona erdi...
    
# tuketim ipi
def tuket(dur, duraklat:Event, kuyruk2):
    # kacirilan ornek sayisi
    n = 0
    
    # baslangic rutini, giris kuyrugu (kuyruk2) doluncaya kadar bekle
    print("Calma baslatildi...")
    while not kuyruk2.full():
        sleep(ornekleme_peryodu)
    
    # durdurma sinyali gelinceye kadar devam et
    while not (dur.is_set()):
        # duraklatma sinyali aktifse bekle
        while duraklat.is_set():
            print("Calma duraklatildi..................................\r", end="")
            sleep(ornekleme_peryodu)
            if dur.is_set(): # durdurma sinyali var
                # duraklatmayi iptal et
                break
        
        # ornek baslangic ani
        bas = perf_counter()
        try:
            # bir ornek kuyruk2 den cekilmeye calisiliyor
            ornek = kuyruk2.get(block = False) 
        except Empty:
            # bir ornek kacti
            print("Kuyruk Bos!")
            ornek = 0
            n = n + 1
            sleep(ornekleme_peryodu) 
            continue
        else:
            sleep(ornekleme_peryodu) # ornekleme suresi
            bit = perf_counter()
            # kuyruktan cekilen is tamamlandi
            kuyruk2.task_done()
            print(f"{ornek} kuyruktan cekildi: sure = ",
                  f"{bit - bas : 2.5f} kuyruk : {kuyruk2.qsize()}")
    
    print(f"Calma sona erdi... Kacirilan ornek sayisi {n} oldu.")

# kuyruk bosaltma rutini
def kuyruk_bosalt(kuyruk):
    while not kuyruk.empty():
        kuyruk.get(block=False)
        kuyruk.task_done()
        
# ana program bolumu
def ana():
    # kuyruk nesneleri tanimlaniyor, 
    kuyruk1   = Queue(maxsize = buf_ebat)
    kuyruk2   = Queue(maxsize = buf_ebat)
    
    # uretim durdu olayi
    dur = Event()

    # uretim duraklat olayi
    duraklat = Event()

    # uretim ipi olusturuluyor
    uret_ip  = Thread(
        target = uret,
        args   = (dur, kuyruk1,)
    )

    # ara ipi olusturuluyor
    ara_ip  = Thread(
        target = ara,
        args   = (dur, kuyruk1, kuyruk2,)
    )

    # tuketim ipi olusturuluyor ve baslatiliyor
    tuket_ip = Thread(
        target = tuket,
        args   = (dur, duraklat, kuyruk2,),
    )

    # ipler baslatiliyor
    uret_ip.start()
    ara_ip.start()
    tuket_ip.start()
    
    # calma baslasin
    sleep(10) # saniye cal
    
    # calma duraklatilsin
    duraklat.set()
    sleep(5)# saniye duraklat
    
    # calma devam etsin
    duraklat.clear()
    sleep(15)# saniye cal
    
    # calma durdurulsun
    dur.set()

    # iplerin tamamlanmasini bekle
    uret_ip.join()
    ara_ip.join()
    tuket_ip.join()
    
    # kuyrukları bosalt ve bekle
    kuyruk_bosalt(kuyruk1)
    kuyruk_bosalt(kuyruk2)
    
    kuyruk1.join()
    kuyruk2.join()
       
if __name__ == '__main__':
    ana()
