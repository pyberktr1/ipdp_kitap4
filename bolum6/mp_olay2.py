# Bu ornek coklu proseslerde olay kullanimini 
# gosteren daha ileri bir ornektir
# olaylarda beklemeyi gosterir

# Proses kutuphanesi
from multiprocessing import Process, Event
# zamanlayici kutuphanesi
from time import sleep
# ip kutuphanesi
from threading import Thread

# Kayitçalar prosesi
def calar(cal, dur):
    # duruncaya kadar devam et
    while not dur.is_set():
        # duraklama var
        # calma olayi 5 sn beklenir
        # 5 sn icinde calma tekrar baslamazsa
        # calma iptal edilir ve kayıtçalar
        # otomatik durdurulur
        if (cal.wait(timeout=5)):
            sleep(0.1)# caliyor
        else:
            dur.set() # durduruluyor

# zamanlayici prosesi
# verilen saniye kadar gecikme sağlar
def zaman(saniye, kapat):
    # verilen saniye kadar gecikme yap
    for i in range(round(saniye*10)):
        # kapatma sinyali geldiyse
        # gecikmeyi derhal iptal et
        if kapat.is_set():
            return
        # 0.1 saniye gecikme ver
        sleep(0.1)  

# komuta prosesi, kayıt çalarlara 
# zamanlanmis komutlar gonderir 
# (cal, duraklat, durdur)      
def kumanda(kanal_sayisi, calmalar, durmalar, kapat):
    # kapatilincaya kadar devam et
    while not kapat.is_set():
        # tum kanallari 2 saniye ara ile duraklat
        for i in range(kanal_sayisi):
            # komut vermeden once bekle
            zaman(2, kapat)
            # ilgili kanali duraklat
            calmalar[i].clear()
            
        # yeni bir komut grubuna baslamadan evvel bekle
        zaman(2, kapat)
        
        # tum kanallari calma durumuna getir 
        for i in range(kanal_sayisi):
            # bir kapatma sinyali varsa hemen kapan
            if kapat.is_set():
                break
            calmalar[i].set() 
            
    # kapanmadan once tum kanallari cal ve dur konumuna getir
    # duraklatilmis kanallar durdurma sinyalini goremeyeceginden
    # kapatmanin derhal algilanmasi icin ilgili kanalin once
    # calma durumuna getirilmesi gerekir
    # aksi halde otomatik durmanin devreye girmesi icin 5 saniye 
    # beklemek gerekir
    for i in range(kanal_sayisi):
        calmalar[i].set()
        durmalar[i].set()

# monitor prosesi    
def monitor(kanal_sayisi, calmalar, durmalar):
    # tum proseslerin baslamasini bekle
    sleep(0.5)
    sn=0.0 # saniye sayaci
    # sonsuz dongude say
    while True:
        # mesaj degiskeni, zamani gosterir
        msj = f"Zaman:{sn:3.2f} san. "
        
        # tum kanal durumlarini izle
        for i in range(kanal_sayisi):
            if durmalar[i].is_set():
                durum = "durdu"
            elif calmalar[i].is_set():
                durum = "caliyor"
            else:
                durum = "durakladi"
            # mesaj hazirlaniyor    
            msj = msj + f"kanal{i}.{durum:10s}::"
        
        print("\r" + msj, end="")
        sleep(0.1) # guncelleme hizi
        sn+=0.1    # saniye sayacini ilerlet
    
# ana program bolumu   
if __name__ == "__main__":
    
    # kapatma sinyali
    kapat = Event()
    
    # kanal sayisi
    kanal_sayisi = 4
    
    # prosesler ve olaylar olusturuluyor
    # her bir kanal basina birer proses ve
    # birer calma ve durdurma olayi tanimlanir
    pler     = []
    calmalar = []
    durmalar = []
    for i in range(kanal_sayisi):
        cal = Event()
        dur = Event()
        cal.set() # calma durumuna getir
        calmalar.append(cal)
        durmalar.append(dur)
        pler.append(Process(target=calar, args=(cal, dur, )))
    
    # gerekli kumanda ve monitor ipleri
    # program sonlanmasinda otomatik kapanma icin 
    # hayalet tipinde acilirlar
    ip1 = Thread(target=kumanda, args=(kanal_sayisi, 
            calmalar, durmalar, kapat, ), daemon=True)
    ip2 = Thread(target=monitor, args=(kanal_sayisi, 
            calmalar, durmalar,), daemon=True)
    # ipler baslatiliyor
    ip1.start()
    ip2.start()
    
    # prosesler baslatiliyor
    for p in pler:
        p.start()
    
    # Enter tusuna basmak programi sonlandirir
    print("BITIRMEK ICIN ENTER'E BASINIZ...")
    input() # Enter bekleyen bos girdi komutu
    kapat.set() # kapatma sinyali aktif
    
    # tum proseslerin kapanmasi bekleniyor
    for p in pler:
        p.join()