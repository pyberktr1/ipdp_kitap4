# bu ornek coklu ipler uzerinde dosyalarla calismayi gosterir

# performans gostergesi
from time import perf_counter, sleep
# test dosyalarini hazirlayan modul
import test_dosya
# ip kutuphanesi
from threading import Thread

# dosya islemlerini gerceklestiren fonksiyon
def degis(dosya, ara, degis):
    print(f"Dosya {dosya} isleniyor\n", end="")
    
    # asagidaki kod blogunu devreye alarak 
    # gorevlerden birisinin takılmasını saglayabiliriz.
    # (bloku devreye almak icin uc tirnak onune bir "#" koyunuz)
    #"""
    if (dosya == "./dosya/test3.txt"):
        sleep(3)
        #"""
        
    # dosya icerigi byte olarak okunuyor
    with open(dosya, 'rb') as d:
        b_metin = d.read()
    # dosya metni string tipe donusturuluyor
    metin = b_metin.decode('utf-8')
    
    # arama islemi yapiliyor
    i = 0
    basla = 0
    while (yer := metin.find(ara, basla)) != -1:
        i += 1
        basla = yer + 1
        
    print(f"{dosya} dosyasinda {i} yerde --{ara}-- metni bulundu. \n", end="")
    
    # degis tokus yapiliyor
    metin = metin.replace(ara, degis)

    # metin byte tipe donusturulerek dosyaya geri yaziliyor
    with open(dosya, 'wb') as d:
        d.write(metin.encode('utf-8'))
        
    print(f"{dosya} ile islem tamamlandi \n", end="")

# ana program blogu 
def ana():
    # test dosyaları hazirlaniyor
    test_dosya
   
   # dosya adlari olusturuluyor
    dosyalar = []

    for i in range (1,11):
        dosyalar.append(f"./dosya/test{i}.txt")

    # create threads
    ipler = [Thread(target=degis, args=(dosya, 'bir', '***ÜÇ***'))
            for dosya in dosyalar]

    # baslangic zamani
    bas = perf_counter()
    
    # ipleri baslatalim
    for ip in ipler:
        ip.start()

    # ip baslatma bitis zamani
    ip_bit = perf_counter()

    # iplerin gorevlerini tamamlamasini bekleyelim
    for ip in ipler:
        ip.join()

    # iplerin bitis zamani      
    bit = perf_counter()

    # report results
    print(f"\n ip baslatmasi : {ip_bit - bas :2.5f} saniye",
          f"\n ip gorevleri  : {bit - ip_bit :2.5f} saniye",
          f"\n toplam sure   : {bit - bas    :2.5f} saniye")
    
    print("Bitirmek icin Entere basiniz...")
    input()

# __main_ ad alanı ile ana program bolumu cagriliyor
if __name__ == "__main__":
    
    # ana program bolumu
    ana()
