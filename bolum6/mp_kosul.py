# Bu ornek kosul kullanimini gosterir 
# her bir tuketici ureticinin urettigi urunler
# icin siraya girer

# coklu proses kutuphanesi
from multiprocessing import Process, Lock, Condition, Queue
# zamanlayici kutuphanesi
import time
# rastgele sayi kutuphanesi
import random
# ip kutuphanesi
from threading import Thread as ip

# uretici prosesi
# firindan ekmek cikaran tek bir uretici vardir
def uretici(sepet, ekmek_mevcut):
    # baslangic gecikmesi
    #time.sleep(2)
    for i in range(5):# baslangic icin 5 ekmek uretiyoruz
        # uretim gecikmesi
        time.sleep(random.uniform(0.1, 0.5))
        # ekmek mevcut kosulu ile kilit atiyoruz
        with ekmek_mevcut:
            # bir ekmek uretildi
            ekmek = f"{i+1} nolu Ekmek"
            # uretilen ekmek sepete atildi
            sepet.put(ekmek)
            print(f"Firinci baba: {ekmek} pisti!")
            # Tuketiciye ekmek pistigini bildiriyoruz
            ekmek_mevcut.notify()  

    # son ekmekler cikariliyor
    for i in range(2):# son olarak tuketici sayisi kadar ekmek uretiyoruz
        # uretim gecikmesi
        time.sleep(random.uniform(0.1, 0.5))
        # ekmek mevcut kosulu ile kilit atiyoruz
        with ekmek_mevcut:
            # bir ekmek uretildi
            ekmek = f"Son Ekmek"
            # uretilen ekmek sepete atildi
            sepet.put(ekmek)
            print(f"Firinci baba: {ekmek} pisti!")
            # Tuketiciye ekmek pistigini bildiriyoruz
            ekmek_mevcut.notify()  

# tuketici prosesi
def tuketici(t_id, sepet, ekmek_mevcut):
    while True:# tum ekmekler bitinceye kadar devam et
        # ekmek mevcut kosulu ile kilit atiyoruz
        with ekmek_mevcut:
            while sepet.empty():# sepette ekmek yoksa siraya gir
                print(f"Musteri {t_id} ekmek bekliyor...")
                ekmek_mevcut.wait()  # ekmek icin bekle
            
            # sepette ekmek var, al onu
            ekmek = sepet.get()
            print(f"Musteri {t_id}: {ekmek} aldi")
            # bu ekmek son ekmek mi?
            if "Son Ekmek" in ekmek:  
                break# ekmek bitti, prosesi sonlandir

# ana program bolumu
if __name__ == "__main__":

    # Global veriyapisi
    # firindan cikan taze ekmeklerin kondugu sepet
    sepet        = Queue()
    # sepete erisimi guvenli hale getiren kilit
    sepet_kilidi = Lock()
    # sepette taze ekmek oldugunu tuketicilere bildiren kosul
    ekmek_mevcut = Condition(sepet_kilidi)
    
    print("FIRINIMIZ ACILMISTIR!")

    # uretici prosesi 
    p1 = Process(target=uretici, args=(sepet, ekmek_mevcut, ))
    p1.start()

    # baslangic gecikmesi
    #time.sleep(1)
    
    # tuketici prosesleri 
    p2 = Process(target=tuketici, args=(1, sepet, ekmek_mevcut, ))
    p2.start()

    p3 = Process(target=tuketici, args=(2, sepet, ekmek_mevcut, ))
    p3.start()

    # proseslerin bitmesini bekle
    p1.join()
    p2.join()
    p3.join()
    
    sepet.close()
    print("FIRINIMIZ KAPANMISTIR!")
