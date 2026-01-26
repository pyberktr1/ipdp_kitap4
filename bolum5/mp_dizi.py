# Bu ornek paylasilmis dizi kullanimini gosterir

# coklu proses kutuphanesi
from multiprocessing import Process, Array

# dizi prosesi
def rezervasyon(no, oda):
    # paylasilmis diziye kilit atiliyor
    with oda.get_lock():
        oda[no] = no + 1
        print(f"Firma No: {no}, {oda[no]} nolu odaya bir rezerve koydu.")

# ana program bolumu
if __name__ == "__main__":
    # 7 oda icin rezervasyon kaydini gosteren paylasilmis
    # dizi yapisi olusturuluyor
    oda = Array('i', 7)
    # prosesler tanimlaniyor
    pler = []
    
    for i in range(7):
        p = Process(target=rezervasyon, args=(i, oda))
        pler.append(p)
        p.start()
    # proseslerin tamamlanmasi bekleniyor    
    for p in pler:
        p.join()
        
    print("\nRezervasyon listesi:")
    print(list(oda))
