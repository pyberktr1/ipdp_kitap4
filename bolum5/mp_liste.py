# Bu ornek yonetici uzerinden liste paylasimini gosterir

# coklu proses kutuphanesi
from multiprocessing import Process, Manager
# rastgele sayi ureteci
import random
# zamanlayici kutuphanesi
import time

# Mesaj kutusu prosesi
def mesaj(kullanici, msj_kutusu, kilit):
    # mesaj gonderme prosesi simule ediliyor
    time.sleep(random.random()*12)# 0-12 saniye rastgele gecikme
    msj = f"{kullanici:7s}: {time.strftime('%H:%M:%S')} aninda bir mesaj atti"

    # bu kisma sadece bir kullanici girebilir
    with kilit:
        msj_kutusu.append(msj)
        print(f"Kullanici {kullanici :7s}: bir mesaj atti!")

# ana program bolumu
if __name__ == "__main__":
    # bir yonetici tanimlaniyor
    with Manager() as yonetici:
        # mesaj kutusu olusturuluyor
        msj_kutusu   = yonetici.list()
        # yonetici uzerinden global bir kilit tanimlaniyor
        kilit        = yonetici.Lock()
        # kullanicilar
        kullanicilar = ["Hasan", "Aysen", "Kerim", "Feride"]
        # prosesler
        pler    = []
        # prosesler tanimlaniyor
        for kullanici in kullanicilar:
            p = Process(target=mesaj, args=(kullanici, msj_kutusu, kilit,))
            pler.append(p)
            p.start()

        # tum proseslerin tamamlanmasini bekleyelim
        for p in pler:
            p.join()

        # Mesaj kutusundaki tum mesajlari listeleyelim
        print("\nMESAJ KUTUSU:")
        print("----------------------------------------------------")
        print()

        for satir in msj_kutusu:
            print(" :::", satir)
        
        # veya alternatif listeleme yontemi
        print("----------------------------------------------------")
        print()
        #print(list(msj_kutusu))
    # yonetici kapatildiktan sonra listeye erisim imkansizdir
    # bu nedenle asagidaki komut gecersizdir
    #print(list(msj_kutusu))   