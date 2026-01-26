# Bu ornek paylasilmis deger kullanimini basitce gosterir

# coklu proses kutuphanesi
from multiprocessing import Process, Value, Lock
# zamanlayici kutuphanesi
import time

# muz paylaşımı prosesi
def muz_proses(isim, muzlar):
    # muzlara kilit atiyoruz
    with muzlar.get_lock():
        # bosta yenilecek muz var mi?
        if muzlar.value > 0:
            # evet muz var
            muzlar.value -= 1 # o muzu ye
            print(f"{isim} bir muz yedi. Kalan muz sayisi: {muzlar.value}")
        else:
            # maalesef muz taze bitti
            print(f"{isim} muz yiyemedi.")

# ana program bolumu
if __name__ == "__main__":
    # 3 tane muzumuz var
    muzlar = Value('i', 3)
    # 4 tane maymun var
    maymunlar = ["Zipir", "Kizil", "Kara", "Saskin"]
    
    # her bir maymun icin birer proses olusturuluyor ve baslatiliyor
    for isim in maymunlar:
        Process(target=muz_proses, args=(isim, muzlar)).start()