# Bu ornek coklu proseslerde olay ve kuyruk kullanimini gosterir
# bir sistem parcayla isini bitirdigi noktada hic beklemeden bir 
# sonraki parcaya gecer. Sistemler arasindaki kuyruklar biriktirme
# gorevini ustlenir

# coklu proses kutuphanesi
from multiprocessing import Process, Event, Queue
# Zaman asimi hatasinda kullanilan "Empty" ve "Full" etiketleri
# multiprocessing kutuphanesinde tanimli olmadigi icin queue
# modülünden cagrilmalidir
from queue import Empty, Full

# zamanlayici kutuphanesi
from time import sleep
# ip kutuphanesi
from threading import Thread as ip

# imalat hatti makine prosesi
# Besleyici, Pres, Boyama ve Firin prosesleri sirayla malzemeyi isler
def makine(isim, giris, cikis):
    # parca değiskeni baslatiliyor
    i = 0
    print(f"{isim} beklemede...")
    # sistem kapanincaya kadar devam et
    kapat = False
    while not kapat:
        # zaman asimi olmadan kuyruktan bir parca cek
        try:
            i = giris.get(timeout=5)
            print(f"{isim} {i} parcasini isliyor!")
            # belli bir noktada ariza meydana getiriyoruz
            #if isim=="Pres" and i==3:
            #    kapat = True
            #    continue
            # normal islem gecikmesi
            sleep(1)
            print(f"{isim} {i} parcasini islemeyi bitirdi!")
        except Empty as error: # kuyrukta zaman asimi oldu
            kapat = True
            continue
        
        # islenen parca cikis kuyruguna (biriktirici) atiliyor
        # zaman asimi varsa ilerideki sistemde bir sikisiklik vardir
        try:
            cikis.put(i, timeout=5)
        except Full as error: # kuyrukta zaman asimi oldu
            kapat = True
    
    # rutinden cikiliyor    
    print(f"{isim} {i} parcasinda zaman asimina ugradi",
           ". \nTum sistemler kapatiliyor...")
    
# zaman sayaci                    
def saat(saat_kapat):
    # zaman sayimi yapiliyor
    i = 0 # saniye sayaci
    # kapanincaya kadar saniyeleri saymaya devam et
    while not saat_kapat.is_set():
        print(f"\033[95mSaniye : {i}\033[00m")
        sleep(1)
        i+=1
                     
# ana program bolumu
if __name__ == "__main__":
    
    # islenecek parca sayisi
    parca_sayisi = 10

    # mekanik sistemler tanimlaniyor
    mek_sis     = ["Besleme", "Pres", "Boyama", "Firin"]
    
    # sistem kuyruklari tanimlaniyor
    # maksimum eleman sayisi parca sayisina esit olacak
    kuyruklar   = [Queue(maxsize=parca_sayisi) for _ in range(len(mek_sis)+1)]
    
    # her bir mekanik sistem icin bir proses tanimlaniyor
    pler = []
    for i in range(len(mek_sis)):
        pler.append(Process(target=makine, args=(mek_sis[i], kuyruklar[i], 
                            kuyruklar[i+1],)))

    # zamanlayici ipi ve durdurma olayi
    saat_kapat = Event()
    saat_ip    = ip(target=saat, args=(saat_kapat, ))
    saat_ip.start()

    # tum prosesler baslatiliyor
    for p in pler:
        p.start()
    
    # baslangic gecikmesi
    # tum proseslerin baslatilmasi bekleniyor
    sleep(1)
    # sistem harekete geciriliyor ve tum parcalar besleme kuyruguna
    # gonderiliyor
    for i in range(parca_sayisi):
        sleep(0.5)
        kuyruklar[0].put(i+1)
        print(f"{i} nolu parca gonderildi...")
    
    # tum proseslerin tamamlanmasi bekleniyor
    # ilk ariza ile birlikte ya da giris kuyrugunda parca kalmadiginda
    # ya da cikis kuyruguna parca atilamadiginda sistem otomatik kapanir
    # ve program sonlanir
    for p in pler:
        p.join()
    
    # zamanlayiciyi durdur 
    saat_kapat.set()
    saat_ip.join()

    # tum kuyruklar kapatiliyor
    for i in range(len(mek_sis)+1):
        kuyruklar[i].close()
    
    print("TUM SISTEMLER DURDU!")