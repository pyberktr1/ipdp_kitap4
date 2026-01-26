# Bu ornek bir ipin olay nesnesi kullanarak nasil
# iptal edilebilecegini gosterir

# ip kutuphanesi
from threading import Thread, Event
# zamanlayici kutuphanesi
from time import sleep

# iptal edilebilir ip fonksiyonu
def gorev(iptal: Event, sonuc):
    kur = ("|","/","-","\\")
    for i in range(10):
        sleep(1)
        print(f"\r ip isletim suresi {i+1} saniye  {kur[i%4]}", end="")
        if iptal.is_set(): # iptal sinyali geldi mi?
            print("\nip iptali gerceklestiriliyor")
            # anormal iptal durumunu bildiren
            # deger geri donduruluyor
            sonuc[0] = -1
            return
    
    # ip normal bir sekilde sonlandiriliyor
    print("\nip normal isletimini tamamladi")
    sonuc[0] = 0
    return

def ana() -> None:
    
    # iptal sinyali tanimlaniyor
    iptal = Event()
    sonuc = [None]
    # ip tanimlaniyor
    ip = Thread(target=gorev, args=(iptal, sonuc,))
    
    # ip baslatiliyor
    ip.start()

    # ipin tamamlanmasi bekleniyor
    # ipin anormal sonlanmasi icin 10 saniyeden
    # kisa bir sure tanimliyoruz
    sleep(3)
    #sleep(8)

    # ipin sonlanmasi icin bir sinyal gonderiyoruz
    if ip.is_alive(): # ip hala canli mi?
        print("\nip iptal edilecek..")
        iptal.set()
    else:
        print("ip canli degil. ip iptali iptal...")
        
    # sonucu alabilmek icin ipin sonlanmasini bekliyoruz
    # bu kismi devreden cikararak sonucun ne oldugunu
    # gormeye calisalim    
    while ip.is_alive():
        pass

    print(f"islem sonucu {sonuc[0]}")

   
if __name__ == '__main__':
    ana()
    
