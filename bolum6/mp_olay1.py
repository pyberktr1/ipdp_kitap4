# Bu ornek coklu proseslerde olay kullanimini gosterir

# coklu proses kutuphanesi
from multiprocessing import Process, Event
# zamanlayici kutuphanesi
from time import sleep
# ip kutuphanesi
from threading import Thread as ip

# imalat hatti makine prosesi
# Besleyici, Pres, Boyama ve Firin prosesleri sirayla malzemeyi isler
def makine(isim, olay, gelecek_olay, kapat_olay):
    i = 0 # parca sayaci
    # kapatma sinyali gelene kadar devam et
    while not kapat_olay.is_set():
        print(f"{isim} beklemede...")
        # hareket sinyali bekleniyor
        # hareket sinyali gecikirse (zaman asimi)
        # sistem kazalari onlemek icin otomatik kapanir
        if (olay.wait(timeout=5)):
            # hareket isareti geldi
            i+=1 # sayaci bir artir
            print(f"{isim} {i} parcasini isliyor!")
            # belli bir noktada ariza meydana getiriyoruz
            #if isim=="Pres" and i==3:
            #    sleep(6)
            # normal islem gecikmesi
            sleep(1)
            print(f"{isim} {i} parcasini islemeyi bitirdi!")
            gelecek_olay.set() # bir sonraki asamayi harekete geciriyoruz
            olay.clear() # hareket sinyalini iptal ediyoruz
        else: # bir ariza meydana geldi, zaman asimi oldu
            print(f"{isim} {i} parcasinda zaman asimina ugradi.", 
                   "\nTum sistemler kapatiliyor...")
            kapat_olay.set()# kapatma sinyali aktif
    
    print(f"{isim} kapandi!")

# zaman sayaci                    
def saat(saat_kapat, kapat_olay):
    # zaman sayimi yapiliyor
    i = 0 # saniye sayaci
    # kapanincaya kadar saniyeleri saymaya devam et
    while not saat_kapat.is_set():
        print(f"\033[95mSaniye : {i}\033[00m")
        sleep(1)
        i+=1
        # 45. saniyede tum sistemi durdur
        if i == 45:
            kapat_olay.set()

# ana program bolumu
if __name__ == "__main__":

    # sistem kapatma olayi tanimlaniyor
    kapat_olay = Event()
    
    # mekanik sistemler tanimlaniyor
    mek_sis    = ["Besleme", "Pres", "Boyama", "Firin"]
    # her bir sistem icin bir harekete gecirme olayi tanimlaniyor
    olaylar    = [Event() for _ in range(len(mek_sis))]
    
    # her bir mekanik sistem icin bir proses tanimlaniyor
    pler       = []
    for i in range(len(mek_sis)):
        pler.append(Process(target=makine, args=(mek_sis[i], olaylar[i], 
                            olaylar[(i+1)%len(mek_sis)], kapat_olay,)))

    # zamanlayici ipi ve durdurma olayi
    saat_kapat = Event()
    saat_ip    = ip(target=saat, args=(saat_kapat, kapat_olay, ))
    saat_ip.start()

    # tum prosesler baslatiliyor
    for p in pler:
        p.start()
    
    # baslangic gecikmesi
    # tum proseslerin baslatilmasi bekleniyor
    sleep(1)
    # ilk sistem harekete geciriliyor
    # ilk domino tasinin devrilmesiyle sistem hareket gecer
    # son sistem parcayla isini tamamladigi noktada ilk sistemi (besleme)
    # yeni bir parca almak uzere tekrar harekete gecirir
    olaylar[0].set()
    
    # tum proseslerin tamamlanmasi bekleniyor
    # ilk ariza ile birlkite sistem otomatik kapanir ve program sonlanir
    for p in pler:
        p.join()
    
    # zamanlayiciyi durdur 
    saat_kapat.set()
    saat_ip.join()

    print("TUM SISTEMLER DURDU!")