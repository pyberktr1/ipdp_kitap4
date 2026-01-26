# bu ornek olay nesneleri araciligi ile iplerarasi
# haberlesmenin nasil gerceklestirilebilecegini gosterir

# ip ve olay kutuphaneleri
from threading import Thread, Event
# zamanlayici kutuphanesi
from time import sleep

def gorev(olay: Event, ipid: int) -> None:
    print(f"ip {ipid} basladi ve beklemede...\n",end="")
    olay.wait()
    print(f"ip {ipid} tamamlandi.")

# ana program bolumu
def main() -> None:
    # bir olay nesnesi olusturuluyor
    olay = Event()
    
    # ipler tanimlaniyor
    ip1 = Thread(target=gorev, args=(olay,1))
    ip2 = Thread(target=gorev, args=(olay,2))

    # ipler baslatiliyor
    ip1.start()
    ip2.start()

    print("Gorevler basladi...")
    # tum gorevlerin tamamlanmasi icin gecikme
    sleep(3) 
    # tum gorevler sonlandiriliyor
    print("Tum gorevler sonlandiriliyor...")
    olay.set()
    
# ana program fonksiyonu __main__ ad alanindan cagriliyor
if __name__ == "__main__":
    main()
