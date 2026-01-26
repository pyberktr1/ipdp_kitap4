# Bu ornek coklu proseslerde kilit kullanimini gosterir

# coklu proses kutuphanesi
from multiprocessing import Process, Lock
# zamanlayici kutuphanesi
import time

# bu proseste bir usta matkap kullanmaya calisiyor
def matkap(usta, kilit):
    
    print(f"{usta} matkabi talep ediyor")

    # belli bir anda sadece bir usta bu bolume girebilir
    with kilit: # duzgun kapatma icin with deyimi kullaniliyor
        print(f"{usta} delme yapiyor...")
        time.sleep(2)  # Delme islemi simüle ediliyor
        print(f"{usta} matkapla isini tamamladi.")

# ana program bolumu
if __name__ == "__main__":

    # matkap erisimini kontrol etmek icin bir kilit tanimlaniyor
    kilit = Lock()
    # atelyedeki ustalar
    ustalar = ["Hayri", "Ahmet", "Necip"]

    # her bir usta icin ayri birer proses aciyoruz ve baslatiyoruz
    for usta in ustalar:
        Process(target=matkap, args=(usta, kilit,)).start()