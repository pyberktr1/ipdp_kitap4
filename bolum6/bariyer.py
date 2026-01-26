# Bu ornek iplerde bariyer kullanimini gosterir 

# zamanlayici kutuphanesi
import time
# rastgele sayi kutuphanesi
import random
# ip kutuphanesi
from threading import Thread as ip
from threading import Barrier

# Bariyer ipi
def bariyer():
    # butun iplerin ilk bariyere ulasmasi bekleniyor
    b_id = b.wait()
    ilk = time.perf_counter()
    print(f"{b_id} ipi ilk bariyeri asti! an:{ilk:2.3f}")
    # rastgele ip islem gecikmesi    
    time.sleep(random.uniform(1,3))
    # ilgili ipin ikinci bariyere ulasma ani
    yetis = time.perf_counter()
    print(f"{b_id} ikinci bariyere ulasti.",
          f"islem suresi:{yetis - ilk : 2.3f} sn.")
    # butun iplerin ikinci bariyere ulasmasi bekleniyor
    b.wait()
    # bariyeri asma ani kaydediliyor
    ikinci = time.perf_counter()
    print(f"{b_id} ipi ikinci bariyeri asti! an:{ikinci:2.3f}")
    
# ana program bolumu
if __name__ == "__main__":
    
    # Global veriyapisi
    # ip sayisi
    ip_say = 3
    # Bariyer tanimi
    b = Barrier(ip_say)
    # ip tanimlari
    ipler = []
    for i in range(ip_say):
        ipi = ip(target=bariyer)
        ipler.append(ipi)

    print("YARIS BASLADI!")    
    # baslangic anini kaydet
    bas = time.perf_counter()
    print(f"Baslangic ani : {bas : 2.3f}")
    
    # tum ipler baslatiliyor
    for i in range(ip_say):
        ipler[i].start()
    
    # tum iplerin bitmesi bekleniyor
    for i in range(ip_say):
        ipler[i].join()

    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"Bitis ani : {bit : 2.3f}")
    print("YARIS BITTI!")
    
    