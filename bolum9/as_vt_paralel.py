# Bu ornek asenkron yapilarda kuyruk kullanimini gostermektedir.
# Bir dizi sorgu uretici konumundaki bir sorgulayacidan tuketici
# konumundaki bir dizi veritabani korosuna bir kuyruk uzerinden
# gonderilmektedir. Toplamda 12 sorgu, ucer ucer gruplar halinde
# 3 veritabani korosuna gonderilmektedir. Burada sonuclanan 
# sorgular ayrica ikinci bir kuyruk ile tekrar sorgulayiciya
# gonderilmektedir. Tum sorgular icin gecen zaman degerlendirilmekte
# ve sonuclanmasi 10 saniyeyi gecen sorgular zamanasimi olarak
# degerlendirilmektedir. Sorgulayici veritabanlarini sorgulamak
# icin gerekli olan seri numarasini "None" olarak girerek
# kapatilmalarini saglamaktadir.

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time
# rastgele deger ureteci
import random

# sorgulayici korosunda kullanilir
zm_asim = 5.0# sorgulama zaman asimi degeri (saniye)
# vt korosunda kullanilir
ariza   = 667# ariza verecek seri no sorgusunu buraya girelim
# veritabani {seri_no: [isim, stok, fiyat]}
vt = {
        311  : ["sigorta", 33, 123],
        124  : ["diyot  ", 13, 221],
        822  : ["disli  ", 25, 155],
        314  : ["anahtar", 45, 673],
        525  : ["ampul  ", 83, 404],
        404  : ["role   ", 66, 531],
        667  : ["kablo  ", 71, 215],
        767  : ["buji   ", 58, 345],
        333  : ["pompa  ", 11, 895]
          }

# ana asenkron koro
async def ana():
    # sorgulama kuyrugu
    sorgu = asyncio.Queue()
    # cevap kuyrugu
    cevap = asyncio.Queue()
    # sorgu listesi, 12'den 3 tanesi hatalidir
    sorgular = [
                311, 124, 503,
                822, 314, 213,
                525, 404, 876,
                667, 767, 333
                ]
    print("***** SORGULAMA BASLADI *****")            
    # baslangic anini kaydet
    bas = time.perf_counter()
    # gorevler olusturuluyor ve birlestiriliyor
    vtler = [] # vt gorevleri
    for i in range(3):
        g = asyncio.create_task(veri(i, sorgu, cevap))
        vtler.append(g)
    # bekleme-birlestirmede istisna kontrolu yapiyoruz
    try:
        await asyncio.gather(
              sorgulayici(sorgu, cevap, sorgular, vtler),
              *vtler, return_exceptions=False
                )
    # gorevlerden birisi istisna dolayisiyla kapanirsa
    # digerleri de otomatik iptal edilir
    # Ancak "return_exceptions" parametresi "True" yapilirsa
    # sorgulayici calismaya devam eder ve kisir dongu olusur
    except* asyncio.CancelledError:# iptal istisnasi olustu
        pass# bos gec
        
    # bitis anini kaydet
    bit = time.perf_counter()
    print("***** SORGULAMA BITTI *****")            
    print(f"Isletim suresi: {bit - bas:2.3f} saniyedir.")

# sorgulayici korosu
async def sorgulayici(sorgu, cevap, sorgular, vtler):

    # tum sorgulari gonder
    for sor in sorgular:
        await sorgu.put(sor)
    
    # tum vtler icin kapanma sinyalini gonder
    for _ in range(3):
        await sorgu.put(None)
        
    # cevaplari al ve raporla
    print()
    print("***** SORGULAMA SONUCLARI *****")
    print("----------------------------" 
          "----------------------------")

    # kapali vt sayisi
    kapali = 0
    
    # sonsuz dongu
    while True:
        
        # baslangic anini kaydet
        # bu an zaman asimi icin referans kabul edilir
        bas = time.perf_counter()
        
        # cevap kuyrugu dolu mu kontrol et
        while cevap.empty():
            await asyncio.sleep(0.1)
            # zamanasimi var mi kontrol et
            if (round(time.perf_counter()-bas,1) > zm_asim):
                print("\033[91mSorgulama esnasinda zamanasimi oldu!\033[0m")
                print("\033[91mTum vtler kapatilacak!\033[0m")
                # vt gorevlerini kapatalim
                for i in range(3):
                    if not vtler[i].done():# gorev tamamlandi mi?
                        vtler[i].cancel()
                # vt gorevleri kapaninca sorgulayici 
                # gorevi de otomatik kapanir ve
                # program buradan ileriye gitmez
        
        # kuyrukta yeni bir cevap var
        cvp = await cevap.get()
        # cevap gecersiz midir?
        if cvp[1]==None:# ilgili vt kapanmis
            kapali+=1
            print(f"\033[93m{cvp[0]} nolu vt kapandi!\033[0m")
            print("----------------------------" 
                  "----------------------------")
            if kapali==3:# tum vtler kapanmis
                print("\033[92mTum Sorgular Basariyla Tamamlandi!\033[0m")
                break
        elif cvp[2]==None:# hatali seri numarasi ile sorgulama var
            print(f"\033[91mvt:{cvp[0]}, {cvp[1]} seri nosunu bulamadi! | "
                  f"sure:{cvp[3]}s\033[0m")
            print("----------------------------" 
                  "----------------------------")
        else:# gecerli bir sorgu sonucu var
            # Elde edilen sonuclari raporlayalim
            print(f"vt:{cvp[0]} :: {cvp[1]} seri nolu parcanin bilgileri:")
            print(f"isim:{cvp[2][0]} | stok:{cvp[2][1]} adet | "
                  f"fiyat={cvp[2][2]}TL | sure:{cvp[3]}s")
            print("----------------------------" 
                  "----------------------------")
                  
    print()
    print("***** SORGULAMA RAPORU SONU *****")
    
# veritabani korosu
async def veri(i, sorgu, cevap):         
    # sonsuza kadar devam et      
    while True:
        # sorgu kuyrugu dolu mu kontrol et
        while sorgu.empty():
            await asyncio.sleep(0.1)
        
        # kuyrukta yeni bir sorgu var
        sno = await sorgu.get()
        # istenilen sorgu "None" ise veri korosunu sonlandir
        if sno is None:
            break
        #print(f"{sno} seri numarali parcanin bilgileri getiriliyor...")
        # islem gecikmesi
        isg = random.uniform(1, 2)
        await asyncio.sleep(isg)
        
        # veritabaninda sorun olusturalim
        if sno==ariza:# ilgili seri numarasinda sorun olusur
            await asyncio.sleep(20)
        
        # seri numarasi veritabaninda var mi?
        if sno in vt:
            #print(f"{sno} seri numarali parcanin verileri bulundu. sure:{isg:2.3f}s")
            # cevabi cevap kuyruguna at
            await cevap.put([i, sno, vt[sno], round(isg,3)])
        else:
            #print(f"Girdiginiz {sno} seri nosu hatalidir! sure:{isg:2.3f}s")
            # cevabi cevap kuyruguna at
            await cevap.put([i, sno, None, round(isg,3)])
            
    # veri korosu kapatiliyor
    #print(f"{i} nolu veritabani kapaniyor...")
    await asyncio.sleep(0.1)
    await cevap.put([i, None, None, None])# kapanmayi sorgulayiciya bildir

# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())