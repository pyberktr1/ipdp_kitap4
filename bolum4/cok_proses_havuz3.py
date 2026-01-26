# bu ornek cok proseste islenen aritmetik
# bir islemin daha hizli gerceklestigini gosterir
# mevcut yekpare prosesi 10 ayri prosese bolerek
# islemleri daha da hizlandirdik
# prosesler proses havuzu kullanarak olusturulmustur
# yekpare proses "chunksize" parametresi ile 
# bolumlendirilmistir. 

# zamanlayici kutuphanesi
import time
# coklu proses havuzu kutuphanesi
from concurrent.futures import ProcessPoolExecutor as pp_icraci

# proses gorevi
def gorev(i):

    # karmasik bir islem yapiliyor
    p = ((((i+0.1)**2)/3.141)**2 + (i+1.2)*1.288**2)**0.5 - (25.5/(i-3.22))**1.148
    
    # sonuc geri donduruluyor
    return p
    
if __name__ == '__main__':
    
    # ise baslangic ani
    bas = time.perf_counter()
    
    # kayıt veri yapisi
    sonuc = []
    
    # araliklar hesaplaniyor
    aralik = 10**7
    aralik_sayisi = 10
    kulce = aralik//aralik_sayisi
    
    # proses havuzu olusturuluyor ve isletime aliniyor
    with pp_icraci() as icraci:
        for cevap in icraci.map(gorev, range(aralik), chunksize=kulce):
            sonuc.append(cevap)
                  
    bit = time.perf_counter()
   
    print(f"Hesaplamanin tamamlanmasi {bit - bas : 3.5f} saniye surdu")
      
    print(sonuc[0])
