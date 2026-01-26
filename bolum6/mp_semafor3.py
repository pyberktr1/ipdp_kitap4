# Bu ornek semafor kullanimini gosterir daha ileri bir ornektir
# kisitli sayidaki yazicilarin zaman paylasimli adil paylasimini 
# gosterir

# coklu proses kutuphanesi
from multiprocessing import Process, Semaphore, Array, Event
# zamanlayici kutuphanesi
from time import sleep
# ip kutuphanesi
from threading import Thread

# yazici isleri prosesi
def yaz_is(kno, sayfalar, yazicilar, yazici):
    # sira basina maximum yazdirma limiti
    max_sayfa = 2
    # ilgili kullanicinin (kno) sayfalari bitinceye kadar devam et    
    while sayfalar[kno]>0:
        # yazici sirasina gir
        with yazici:# bosta yazici semaforu yoksa bekle
            # yaziciyi kullaniciya ata
            with yazicilar.get_lock():
                if 1 not in yazicilar:   # 1 nolu yazici bosta mi?
                    yazicilar[kno]=1
                elif 2 not in yazicilar: # 2 nolu yazici bosta mi?
                    yazicilar[kno]=2
                elif 3 not in yazicilar: # 3 nolu yazici bosta mi?
                    yazicilar[kno]=3
                    
            # maximum sayfa limitine kadar yazdir
            for i in range(max_sayfa):
                # sayfa basina yazdirma suresi
                sleep(1.5)
                # yazdirilan sayfayi hesaptan dus
                sayfalar[kno]-=1
                if sayfalar[kno]==0:
                    # yazdirilacak sayfa kalmadi
                    break# gorevi sonlandir
            
            # yaziciyi gorevden al
            with yazicilar.get_lock():
                yazicilar[kno]=0
                
# yazdirma durumu monitoru        
def monitor(n_kullanici, sayfalar, yazicilar):
    san=0.0 # saniye sayaci
    # program kapanincaya kadar devam et
    while True:
        # ekran mesajini hazirla
        # saniyeyi goster
        msj = f"Zaman:{san:3.2f} san. "
        
        # tum kullanici durumlarini takip et
        for i in range(n_kullanici):
            # aktiflesen is kirmiziya boyanir
            if yazicilar[i]>0:
                renk = 91
            else:
                renk = 0
            msj = msj + f"\033[{renk}m{yazicilar[i]}/{i}/{sayfalar[i]}\033[00m::"
            
        # mesaj ekrana yazdiriliyor
        print("\r" + msj + "          ", end="")
        # tazeleme gecikmesi
        sleep(0.1)
        # saniye sayacini artir
        san+=0.1
    
# ana program bolumu   
if __name__ == "__main__":

    print("YAZICI DURUMU...")
    print("Yazici/Kullanici/Kalan Sayfa")
    
    # yazici sayisi
    n_yazici    = 3
    # kullanici sayisi
    n_kullanici = 5  
    # her bir kullanicinin yazdiracagi sayfa sayilari
    sayfalar    = Array("i", [5, 7, 8, 9, 3])
    # kullanicilara hangi yazicinin atandigini gosteren yapi
    # ilgili kullaniciya ait hucre sifir degerini gosteriyorsa
    # o kullaniciya herhangi bir yazici atanmamis demektir
    yazicilar   = Array("i", n_kullanici)
    
    # Sadece 3 yazici var
    yazici = Semaphore(n_yazici)
    
    # her bir kullaniciya birer proses ataniyor
    pler = []
    for i in range(n_kullanici):
        pler.append(Process(target=yaz_is, args=(i, 
                     sayfalar, yazicilar, yazici,)))
    
    # monitor ipi, ekrana bilgilendirme mesajlarini yazar
    # hayalet tipinde oldugu icin program kapanisi ile 
    # birlikte otomatik kapanir
    ip1 = Thread(target=monitor, args=(n_kullanici, 
                    sayfalar, yazicilar,), daemon=True)
    
    # monitor ipi baslatiliyor
    ip1.start()
    
    # prosesler baslatiliyor
    for p in pler:
        p.start()

    # proseslerin bitmesi bekleniyor
    for p in pler:
        p.join()
    
    # monitor ipi kapanma gecikmesi
    sleep(1)