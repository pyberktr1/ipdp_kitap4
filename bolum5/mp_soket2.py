# Bu ornek soket uzerinden cift yonlu mesaj paylasimini gosterir

# coklu proses kutuphanesi
from multiprocessing import Process
# soket kutuphanesi
import socket
# zamanlayici kutuphanesi
from time import sleep

# sunucu prosesi (once alici sonra gonderici)
def sunucu():
    # sokete dinleme icin giris baglantisi yapiliyor
    s_giris = socket.socket()
    # soket dinleme icin aciliyor
    s_giris.bind(("localhost", 12345))
    s_giris.listen(1)
    # bag ve adres aliniyor
    bag, adr = s_giris.accept()
    
    # veri gonderimi icin bir soket nesnesi tanimlaniyor
    s_cikis = socket.socket()
    # sokete gonderme icin baglaniliyor
    s_cikis.connect(("localhost", 12346))

    # soketten gelen veri paketi cekiliyor
    print(bag.recv(1024).decode())
    # bekleme yapiliyor
    sleep(2)
    
    # bir veri paketi gonderiliyor (1024 bayttan az)
    s_cikis.send(b"Hizmetciden Merhaba!")
    
    # is bittikten sonra tum baglantilar kapatilmalidir
    bag.close()
    s_cikis.close()

# istemci prosesi (once gonderme sonra alma)
def istemci():
    # once bekle
    sleep(2)
    # gonderme icin bir soket tanimlaniyor
    s_cikis = socket.socket()
    # sokete baglaniliyor
    s_cikis.connect(("localhost", 12345))
    
    # alma icin bir soket nesnesi tanimlaniyor
    s_giris = socket.socket()
    # soket nesnesine alma icin baglaniliyor
    s_giris.bind(("localhost", 12346))
    s_giris.listen(1)
    # bag ve adres aliniyor
    bag, adr = s_giris.accept()

    # soketten bir veri paketi gonderiliyor (1024 bayttan az)
    s_cikis.send(b"Musteriden Merhaba!")
    
    # karsidan alinan veri paketi yazdiriliyor
    print(bag.recv(1024).decode())

    # is bittikten sonra tum baglantilar kapatilmalidir
    bag.close()
    s_cikis.close()

# ana program bolumu
if __name__ == "__main__":
    
    print("ALMA VE GONDERME BASLIYOR")
    
    # prosesler tanimlaniyor
    p1 = Process(target=sunucu)
    p2 = Process(target=istemci)
    
    # prosesler baslatiliyor
    p1.start()
    p2.start()
    
    # proseslerin tamamlanmasi bekleniyor
    p1.join()
    p2.join()

    print("ALMA VE GONDERME TAMAMLANDI")