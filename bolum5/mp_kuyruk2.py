# Bu ornek coklu proseslerde kuyruk ile yapilan haberlesmelerde
# yon olmadigini dolayisiyla ayni proses icinde hem okuma hem de
# yazma yapilmasi durumunda problem yasanacagini gostermektedir
# cift yonlu haberlesme icin iki kuyruk ayri ayri kullanilmali
# veya uygun bir yon kontrol protokolu belirlenmelidir.

# coklu proses kutuphanesi
import multiprocessing as mp
# zamanlayici kutuphanesi
import time

# yazici prosesi
def yazici(kuyruk):
    print("\nYaziliyor...")
    time.sleep(5)
    # kuyruga yaziliyor
    kuyruk.put("Yazicidan merhaba")
    # kuyruktan okuma yapiliyor
    msj = kuyruk.get()
    print(f"\nYazicidan Alinan: {msj}")

# okuyucu prosesi
def okuyucu(kuyruk):
    print("\nOkunuyor...")
    # okuma kasitli olarak geciktiriliyor
    #time.sleep(7)
    # kuyruktan okumma yapiliyor
    msj = kuyruk.get()
    print(f"\nOkuyucudan Alinan: {msj}")
    time.sleep(1)
    # kuyruga iki mesaj ekleniyor ama sadece biri cekilecek
    kuyruk.put("Okuyucudan merhaba")
    kuyruk.put("Okuyucudan tekrar merhaba")

# ana program bolumu
if __name__ == '__main__':
    #  bir kuyruk olusturuluyor
    kuyruk = mp.Queue()

    # prosesler olusturuluyor
    p1 = mp.Process(target=yazici,  args=(kuyruk,))
    p2 = mp.Process(target=okuyucu, args=(kuyruk,))

    # prosesler baslatiliyor
    p1.start()
    p2.start()
    
    # zaman sayimi yapiliyor
    for i in range(10):
        print(f"\rSaniye : {i}", end="")
        time.sleep(1)
    
    # proseslerin tamamlanmasi bekleniyor
    p1.join()
    p2.join()
    
    # kuyruk kapatilmadan evvel bosaltilmalidir
    
    print("\nKuyruk bosaltiliyor...")
    while not kuyruk.empty(): # kuyruk bosalincaya kadar devam et
        print(kuyruk.get())
    
    # bos kuyruk kapatilmalidir
    kuyruk.close()