# bu ornek cok proseste islenen aritmetik
# bir islemin daha hizli gerceklestigini gosterir
# mevcut yekpare prosesi 10 ayri prosese bolerek
# islemleri daha da hizlandirdik

# zamanlayici kutuphanesi
import time
# coklu proses kutuphanesi
import multiprocessing

# proses gorevi
def gorev(araliklar, pid, kuyruk):
    # kayit veri yapisi
    sonuc = []

    # uzun bir for dongusu ile yogun hesap yapiliyor
    for i in range(araliklar[0], araliklar[1]):
        # karmasik bir islem yapiliyor
        p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
        sonuc.append(p)
    
    # sonuc kuyruga atiliyor
    kuyruk.put({pid : sonuc})
    
if __name__ == '__main__':
    
    # ise baslangic ani
    bas = time.perf_counter()
    
    # kayıt veri yapisi
    sonuc = []
    
    kuyruk = multiprocessing.Queue()

    # araliklar hesaplaniyor
    araliklar = []
    # carpan ve aralik sayisi
    aralik_sayisi = 10
    aralik = 10**7//aralik_sayisi
    for i in range(0, aralik_sayisi):
        araliklar.append([i*aralik, (i+1)*aralik])

    # prosesler
    pler = []
    
    # prosesler tanimlaniyor
    for i in range(aralik_sayisi): # 10 bolum
        pler.append(multiprocessing.Process(target=gorev, 
                                            args=(araliklar[i], i, kuyruk, )))

    # prosesler baslatiliyor
    for i in range(aralik_sayisi):
        pler[i].start()
    
    # sonuclar proseslerden cekiliyor
    sozluk = {}
    for i in range(aralik_sayisi):
        sozluk.update(kuyruk.get())
    
    # sozlukteki veri bloklari siralarina gore sonuc listesine ekleniyor
    for i in range(aralik_sayisi):
        deger = sozluk.pop(i, None)
        if deger == None:
            print("Veri hatasi! ", deger)
        else:
            sonuc = sonuc + deger
    
    bit = time.perf_counter()
   
    print(f"Hesaplamanin tamamlanmasi {bit - bas : 3.5f} saniye surdu")
    
    print(sonuc[0])
