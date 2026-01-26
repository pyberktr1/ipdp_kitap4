# Bu ornekte borularin coklu proses haberlesmesinde 
# nasil kullanildigi gosterilmektedir

# proses kutuphanesi
import multiprocessing as mp
# zamanlayici kutuphanesi
import time

# verici prosesi
def verici(boru):
    print("\nGonderim yapiliyor...")
    time.sleep(5)
    # bir mesaj boru araciligi ile iletiliyor
    boru.send("Vericiden merhaba!")
    # isi biten boru her zaman kapatilmalidir
    boru.close()

# Alici prosesi
def alici(boru):
    print("\nAliniyor...")
    time.sleep(6)
    # bir mesaj aliniyor
    msj = boru.recv()
    print(f"\nAlinti: {msj}")

# ana program bolumu
if __name__ == '__main__':
    # alici ana taraf, verici alt taraf olmak uzere
    # bir boru tanimlaniyor
    ana_boru, alt_boru = mp.Pipe()
    
    # prosesler tanimlaniyor
    p1 = mp.Process(target=verici, args=(alt_boru,))
    p2 = mp.Process(target=alici,  args=(ana_boru,))
    
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
