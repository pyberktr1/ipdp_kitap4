# bu ornek cok proseste islenen aritmetik
# bir islemin daha hizli gerceklestigini gosterir
# mevcut yekpare prosesi 10 ayri prosese bolerek
# islemleri daha da hizlandirdik
# prosesler proses havuzu kullanarak olusturulmustur

# zamanlayici kutuphanesi
import time
# coklu proses havuzu kutuphanesi
from concurrent.futures import ProcessPoolExecutor as pp_icraci

# proses gorevi
def gorev(araliklar, pid):
    # kayit veri yapisi
    sonuc = []

    # uzun bir for dongusu ile yogun hesap yapiliyor
    for i in range(araliklar[0], araliklar[1]):
        # karmasik bir islem yapiliyor
        p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
        sonuc.append(p)
    
    # sonuc geri donduruluyor
    soz = [pid, sonuc]
    return soz
    
if __name__ == '__main__':
    
    # ise baslangic ani
    bas = time.perf_counter()
    
    # kayıt veri yapisi
    sonuc = []
    
    # araliklar hesaplaniyor
    araliklar = []
    pidler    = []
    # carpan ve aralik sayisi
    aralik_sayisi = 10
    aralik = 10**7//aralik_sayisi
    for i in range(0, aralik_sayisi):
        araliklar.append([i*aralik, (i+1)*aralik])
        pidler.append(i)
    
    # proses id listesi (isletim sirasina gore)
    pid_liste = [] 
    
    # proses havuzu olusturuluyor ve isletime aliniyor
    with pp_icraci() as icraci:
        cevaplar = icraci.map(gorev, araliklar, pidler)
        
        # cevaplar isletim sirasina gore aliniyor
        # burada sorgulama tamamlanma sirasina gore degil de 
        # isletime alma sirasina gore oldugu icin elde
        # edilen sonuc listesi halihazirda siralanmis bicimde 
        # geliyor
        for cevap in cevaplar:
            pid_liste.append(cevap[0])
            sonuc = sonuc + cevap[1]

            
    bit = time.perf_counter()
   
    print(f"Hesaplamanin tamamlanmasi {bit - bas : 3.5f} saniye surdu")
    
    # sonuclarin elde edilme sirasi sunuluyor
    # sonuclarin her seferinde sirali geldigine dikkat edin
    print(pid_liste)
    
    print(sonuc[0])
