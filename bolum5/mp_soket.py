# Bu ornek soket uzerinden mesaj paylasimini gosterir

# coklu proses kutuphanesi
from multiprocessing import Process
# soket kutuphanesi
import socket

# sunucu proses (alici taraf)
def sunucu():
    # bir soket nesnesi tanimlaniyor
    s = socket.socket()
    # localhost:127.0.0.1 adresinde 12345 nolu port
    # dinleme icin aciliyor
    s.bind(("localhost", 12345))
    print("dinleme soketi: ",s.getsockname())
    s.listen(1)
    # bag ve adres aliniyor
    bag, adr = s.accept()
    print("alim soketi: ",bag)
    print("alim adresi: ",adr)
    # alinan veri paketi yazdiriliyor
    print(bag.recv(1024).decode())
    # is bittikten sonra baglanti mutlaka kapatilmalidir
    bag.close()

# istemci proses (gonderici taraf)
def istemci():
    # bir soket nesnesi tanimlaniyor
    s = socket.socket()
    # lokal agda 12345 nolu porta gonderim icin baglaniliyor
    s.connect(("localhost", 12345))
    print("verim soketi  : ",s.getsockname())
    # bir veri paketi (1024 bayttan az) gonderiliyor
    s.send(b"Musteri merhaba diyor!")
    # is bittikten sonra soket mutlaka kapatilmali
    s.close()
# ana program bolumu
if __name__ == "__main__":
    # gonderim basliyor
    print("GONDERIM BASLIYOR!")    
    
    # prosesler tanimlaniyor
    p1 = Process(target=sunucu)
    p2 = Process(target=istemci)
    # prosesler baslatiliyor
    p1.start()
    p2.start()
    # proseslerin bitmesi bekleniyor
    p1.join()
    p2.join()

    # gonderim tamam
    print("GONDERIM SONU!")