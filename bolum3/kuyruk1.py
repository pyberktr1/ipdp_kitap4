# bu ornek biri uretici digeri tuketici iki ip
# arasinda bir kuyruk araciligi ile nasil veri
# paylasilabilecegini gostermektedir

# zamanlayici kutuphanesi
from time import sleep, perf_counter
# kuyruk kutuphanesi
from queue import Queue, Full, Empty
# ip kutuphanesi
from threading import Thread, Event

# uretici ipi
def uret(uret_son:Event, kuyruk):
    n = 0 # dusurulen ornek sayisi
    # 100 adet ornek uretilecek
    for i in range(1, 101):
        # ornek baslangic ani
        bas = perf_counter()
        try:
            sleep(0.5) # ornekleme suresi
            # bir ornek kuyruga eklenmeye
            # calisiliyor
            kuyruk.put(i, block = False)
        except Full:
            print("\033[91mKuyruk Dolu!\033[0m")
            n = n + 1
            continue
        else:
            bit = perf_counter()
            print(f"\033[91m{i} ornegi kuyruga eklendi: sure = ",
                  f"{bit - bas : 2.5f} kuyruk : {kuyruk.qsize()}\033[0m")
    print(f"\033[91mUretim sona erdi... Dusen ornek sayisi {n} oldu\033[0m")
    uret_son.set()

# tuketim ipi
def tuket(uret_son:Event, kuyruk):
    # tutulan ornek sayisi
    n = 0
    # tum ornekler kuyruktan cekilinceye
    # veya uretim duruncaya kadar devam et
    while not (kuyruk.empty() and uret_son.is_set()):
        # ornek baslangic ani
        bas = perf_counter()
        try:
            # bir ornek cekilmeye calisiliyor
            ornek = kuyruk.get(block = False) 
        except Empty:
            print("Kuyruk Bos!")
            sleep(0.125) # ip bosta gecikmesi
            continue
        else:
            n = n + 1
            sleep(0.25) # ornekleme suresi
            # sleep(0.5)  # ek ornekleme suresi
            bit = perf_counter()
            print(f"{ornek} kuyruktan cekildi: sure = ",
                  f"{bit - bas : 2.5f} kuyruk : {kuyruk.qsize()}")
            # kuyruktan cekilen is tamamlandi
            kuyruk.task_done()
    print(f"Tuketim sona erdi... Tutulan ornek sayisi {n} oldu.")

# ana program bolumu
def ana():
    # kuyruk nesnesi, max derinlik 10 eleman
    # derinliği sonsuz yapmak icin parantezi bos birakin
    # veya maxsize parametresini sifir ya da sifirdan
    # kucuk verin.
    kuyruk   = Queue(maxsize = 10)
    # uretim durdu olayi
    uret_son = Event()

    # uretim ipi olusturuluyor ve baslatiliyor
    uret_ip  = Thread(
        target = uret,
        args   = (uret_son, kuyruk,)
    )
    uret_ip.start()

    # tuketim ipi olusturuluyor ve baslatiliyor
    tuket_ip = Thread(
        target = tuket,
        args   = (uret_son, kuyruk,),
    )
    tuket_ip.start()

    # iplerin tamamlanmasini bekle
    uret_ip.join()
    tuket_ip.join()

    # tum ipler tamamlandiginda kuyruktaki isler de
    # tamamlanmis olacaktir. Ancak garanti olsun diye
    # kuyrugun da tamamlanmasini bekliyoruz.
    kuyruk.join()


if __name__ == '__main__':
    ana()
