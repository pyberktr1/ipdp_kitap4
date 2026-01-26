# Bu ornekte bir borunun çift tarafli yani
# hem gonderim hem alim modunda kullanimi
# gosterilmektedir

# proses kutuphanesi
import multiprocessing as mp
# zamanlayici kutuphanesi
import time

# verici prosesi
def verici(boru):
    # borunun is bittikten sonra duzgunce kapanmasi icin
    # with bloku icinde kullanimi gerceklestiriliyor
    with boru as b:
        print("\nGonderiliyor...")
        time.sleep(5)
        # bir gonderim yapiliyor
        b.send("Vericiden merhaba!")
        # karsidan gelecek cevap icin dinleme moduna geciliyor
        # karsidan hic cevap gelmezse proses kilitlenir
        msj = b.recv()
        print(f"\nVericide Alinan: {msj}")

# alici prosesi
def alici(boru):
    with boru as b:
        print("\nAliniyor...")
        # kasitli olarak alim geciktiriliyor
        # ancak boru tamponunda yer oldugu muddetce 
        # gonderici tarafta bekleme olmaz
        # tampon doldugunda gonderici yeni bir yer
        # acilincaya veya zamanasimi oluncaya kadar bekler
        #time.sleep(7)
        msj = b.recv()
        print(f"\nAlicida Alinan: {msj}")
        time.sleep(1)
        # iki gonderiden sadece biri alinacak
        # alinmayan gonderiden dolayi boru tamponu dolmadikca
        # gondericide bekleme olmaz
        # borularin dolulugunu test etme imkanimiz olmadigindan
        # kapatmadan evvel bosaltma sansina da sahip degiliz.
        b.send("Alicidan merhaba")
        b.send("Alicidan tekrar merhaba")

# ana program bolumu
if __name__ == '__main__':
    # boru iki tarafli olarak aciliyor
    ana_boru, alt_boru = mp.Pipe()
    
    # prosesler tanimlaniyor
    p1 = mp.Process(target=verici, args=(alt_boru,))
    p2 = mp.Process(target=alici,  args=(ana_boru,))

    # proseler baslatiliyor
    p1.start()
    p2.start()
    
    # zaman sayaci sayiyor
    for i in range(10):
        print(f"\rSaniye : {i}", end="")
        time.sleep(1)
    
    # proseslerin tamamlanmasi bekleniyor
    p1.join()
    p2.join()
