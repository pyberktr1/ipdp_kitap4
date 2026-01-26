# bu ornek tek ip uzerinde dosyalarla calismayi gosterir

# performans gostergesi
from time import perf_counter
# test dosyalarini hazirlayan modul
import test_dosya

# dosya islemlerini gerceklestiren fonksiyon
def degis(dosya, ara, degis):
    print(f"Dosya {dosya} isleniyor")
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

    print(f"{dosya} dosyasında islem tamamlandi...")


# ana program blogu
def ana():
    # dosya adlari olusturuluyor
    dosyalar = []

    for i in range (1,11):
        dosyalar.append(f"./dosya/test{i}.txt")
    
    # dosyalarda degisim gerceklestiriliyor
    for dosya in dosyalar:
        degis(dosya, 'bir', '***ÜÇ***')

# __main__ ad alanı ile ana program bolumu cagriliyor
# dogrudan isletim durumunda asagidaki kisim isletilir
# modul halinde import edilmesi durumunda bu kisim isletilmez
if __name__ == "__main__":
    
    # test dosyaları hazirlaniyor
    test_dosya
    
    # baslangic zamani
    bas = perf_counter()
    # ana program bolumu
    ana()
    # bitis zamani
    bit = perf_counter()
    print(f'Program isletimi {bit - bas :2.5f} saniye surdu.')
