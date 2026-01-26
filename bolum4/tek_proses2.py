# bu ornek tek proseste islenen aritmetik
# bir islemin ne kadar yavas gerceklestigini gosterir
# islemler bir dizi araliga bolunuyor

# zamanlayici kutuphanesi
import time

# proses gorevi
def gorev(araliklar):
    # uzun bir for dongusu ile yogun hesap yapiliyor
    for k in range(len(araliklar)):
        for i in range(araliklar[k][0], araliklar[k][1]):
            # karmasik bir islem yapiliyor
            p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
            sonuc[i] = p
    
if __name__ == '__main__':

    # ise baslangic ani
    bas = time.perf_counter()
    
    # kayıt veri yapisi
    sonuc = []
    [sonuc.append(0) for _ in range(10**7)]

    # araliklar hesaplaniyor
    araliklar = []
    # carpan ve aralik sayisi
    aralik_sayisi = 10
    aralik = 10**7//aralik_sayisi
    for i in range(0, aralik_sayisi):
        araliklar.append([i*aralik, (i+1)*aralik])
    
    gorev(araliklar)
    bit = time.perf_counter()

    print(f"Hesaplamanin tamamlanmasi {bit - bas : 3.5f} saniye surdu")

    print(sonuc[0])
