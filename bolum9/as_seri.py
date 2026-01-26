# Bu ornek kollektif calisma gosteren bir dizi asenkron koro
# uzerinde seri calisma sistemini gosterir.
# Bu ornekte bir dizi otomobil yedek parcasina ait 3 farkli
# veritabani uzerinde seri-ardisik sorgulamalarin asenkron 
# bir yapi cercevesinde ayni zamanli eldesine yonelik islemler
# gerceklestirilmektedir. Her bir parcanin sorgulamasi ayni zamanli
# yapilmakla beraber, her bir veritabanindaki sorgulamalar ayni parca
# icin ardisik bir sirada gerceklestirilmektedir. ilk sorgulama diger
# sorgulamalari otomatik baslatmaktadir.
# Bir parca icin once seri numarasi ile aciklama verisi sorgulanmakta,
# ardindan buradan gelen stok numarasi ile stok verisi alinmakta ve
# en son stok kodu ile fiyat veritabanindan fiyat cekilmektedir.
# her bir sorgulama bir onceki sorgulamadan gelen verilere ihtiyac
# duydugundan sirali bir sekilde yapilmak zorundadir.
# her bir veritabanina ait sorgulamalar her bir parca icin farkli
# surelerle sonuclanmakta ancak 5 parca icin yapilan sorgulamalar
# ayni zamanli gerceklestiginden toplam islem suresi her bir sorgulamanin
# toplamindan daha kisa surmektedir.

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time
# rastgele deger ureteci
import random

# ana asenkron govde
async def ana():
    # sorgulanacak parca seri nolari
    # 11 seri nosu hatali seri nosudur
    seri_nolar = [3, 7, 13, 23, 33, 11]
    # baslangic anini kaydet
    bas = time.perf_counter()
    # sorgulama baslatma cagrisi
    s = await asyncio.gather(*(veri_getir(seri_no) for seri_no in seri_nolar))
    # bitis anini kaydet
    bit = time.perf_counter()
    
    # sonuc raporu
    print()
    print("***** SORGULAMA SONUCLARI *****")
    print(f"{len(s)} adet sorgu icin",
          f"toplam isletim suresi: {bit - bas:2.3f} saniyedir")
    print()
    print("***** RAPOR BASI *****")
    print("-------------------------------------" 
          "-------------------------------------")
    for i in range(len(s)):
        # Elde edilen sonuclari raporlayalim
        print(f"{s[i]["seri_no"]} seri nolu parcanin sorgulama bilgileri:")
        print(f"isim:{s[i]["isim"]} | stok_no:{s[i]["stok_no"]} | "
              f"stok:{s[i]["stok"]} adet | "
              f"stok_kod:{s[i]["stok_kod"]} | fiyat={s[i]["fiyat"]}TL")
        print("-------------------------------------" 
              "-------------------------------------")
    print("***** RAPOR SONU *****")

# veri sorgulamasi baslaticisi
async def veri_getir(seri_no):
    # ilk sorgulama ile parca ismi getirilir
    stok_no , isim = await isim_getir(seri_no)
    # ikinci sorgulama ile stok verisi alinir
    stok_kod, stok = await stok_getir(stok_no)
    # son sorgulama fiyat bilgisini verir
    fiyat          = await fiyat_getir(stok_kod)
    
    return {"seri_no":seri_no, "isim":isim, 
            "stok_no":stok_no, "stok_kod":stok_kod,
            "stok":stok, "fiyat":fiyat}
    
# parca ismi sorgulayici
async def isim_getir(seri_no):
    # veritabani {seri_no: [stok_no,isim]}
    vt = {
          3  : [1233, "sigorta"],
          7  : [1234, "diyot  "],
          13 : [1235, "buji   "],
          23 : [1236, "disli  "],
          33 : [1237, "anahtar"]
          }
          
    # islem gecikmesi
    i = random.uniform(1.0, 2.0)
    print(f"{seri_no=} parcanin isim bilgileri getiriliyor...")
    await asyncio.sleep(i)
    if seri_no in vt:
        print(f"{seri_no=} isim bilgileri basariyla getirildi. sure:{i:2.3f}s")
        return vt[seri_no]
    else:
        print(f"Girdiginiz {seri_no=} hatalidir! sure:{i:2.3f}s")
        return [None, None]

# parca stok sorgulayici
async def stok_getir(stok_no):
    # veritabani {stok_no: [stok_kod,stok]}
    vt = {
          1233 : [313, 51],
          1234 : [525, 25],
          1235 : [373, 75],
          1236 : [555, 13],
          1237 : [741, 43]
          }
          
    # islem gecikmesi
    i = random.uniform(1.0, 2.0)
    print(f"{stok_no=} parcanin stok bilgileri getiriliyor...")
    await asyncio.sleep(i)
    if stok_no in vt:
        print(f"{stok_no=} Stok bilgileri basariyla getirildi. sure:{i:2.3f}s")
        return vt[stok_no]
    else:
        print(f"Girdiginiz {stok_no=} hatalidir! sure:{i:2.3f}s")
        return [None, None]

# parca fiyat sorgulayici
async def fiyat_getir(stok_kod):
    # veritabani {stok_kod : fiyat}
    vt = {
          313: 351,
          525: 215,
          373: 165,
          555: 823,
          741: 983
          }
          
    # islem gecikmesi
    i = random.uniform(1.0, 2.0)
    print(f"{stok_kod=} parcanin fiyat bilgileri getiriliyor...")
    await asyncio.sleep(i)
    if stok_kod in vt:
        print(f"{stok_kod=} Fiyat bilgileri basariyla getirildi. sure:{i:2.3f}s")
        return vt[stok_kod]
    else:
        print(f"Girdiginiz {stok_kod=} hatalidir! sure:{i:2.3f}s")
        return None

# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
    