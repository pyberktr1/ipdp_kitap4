# Bu ornek coklu proseslerde kuyruklarin proseslerarasi
# haberlesmede nasil kullanildigini gostermektedir

# coklu proses kutuphanesi
import multiprocessing as mp
# zamanlayici kutuphanesi
import time

# yazici prosesi
def yazici(kuyruk):
    print("\nYaziliyor...")
    time.sleep(5)
    # kuyruga bir mesaj atiliyor
    kuyruk.put("Yazicidan merhaba!")

# Okuyucu prosesi
def okuyucu(kuyruk):
    print("\nOkunuyor...")
    # kuyruktan bir mesaj cekiliyor
    msj = kuyruk.get()
    print(f"\nAlinan: {msj}")

# ana program bolumu
if __name__ == '__main__':
    # Bir kuyruk olusturuluyor
    kuyruk = mp.Queue()

    # prosesler tanimlaniyor
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
    
    # kuyruk nesneleri with ile kontrol saglamadigindan
    # manuel olarak kapatilmalidir
    kuyruk.close()