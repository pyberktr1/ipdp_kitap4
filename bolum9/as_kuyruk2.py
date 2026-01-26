# Bu ornek bir harddisk ve ses karti arasinda kopru gorevi goren
# bir kuyrugun kullanildigi bir asenkron prosesi gostermektedir.
# harddisk 10 ms erisim suresi ile her bir batinda 4kb 
# (hesap kolayligi icin 1kb = 1000 bayt kabul ediliyor) veri
# aktarmaktadir. Harddisk 1 saniyede 400kb veri sunabilmektedir.
# Ses karti ise 8-bitte (ornek basina 1 bayt) saniyede 40kb veri
# tuketmektedir (ornekleme hizi 40KHZ). Ses karti her 20 ms de bir 
# tampon bellegini taze veri ile doldurmak icin talepte bulunmaktadir.
# Buna gore ses karti en az 40000 bayt/s / 50 tazeleme/s = 800 bayt/tazeleme 
# hız sağlamalıdır. Yani 20 ms icinde 800 bayt veri ile beslenmelidir. 
# Bu besleme hizi saglanamadigi takdirde ornek dusmesi yasanmakta ve 
# calinan seste kisa sureli sessiz bolumler olmaktadir.
# Harddisk saniyede 400kb saglayabildiginden dolayi normal sartlarda
# herhangi bir sorun yasanmayacaktir. Ancak siradisi harddiski asiri mesgul
# eden bir durum erisim suresini anormal sekilde yukseltirse aradaki
# tampon bellek bosalacak ve ornek dusumu yasanacaktir.
# Bu durumun yasanma ihtimalini azaltmak maksatli tampon bellek ebati
# 1 saniyelik ornek saglayacak bir derinlikte (40kb) olarak dusunulmustur.
# Harddiskten veriler 4kblik paketler halinde geldiginden tampon bellek 
# ebadi 40kb / 4kb = 10 eleman olacak sekilde ayarlanmistir. Ses karti
# da verileri 4kB'lik paketler halinde alir ve bu da tazeleme hizini
# 20ms x (4000 / 800) = 100 ms seklinde guncelleme zorunlulugu getirir.

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# harddisk modeli
async def disk(erisim_suresi):
    # erisim suresi kadar bekleme
    await asyncio.sleep(erisim_suresi)

# harddiskten veri getirme korosu
async def verici(tampon, erisim_suresi):
    paket = [33]*4000#4 kblik paket
    while True:# sonsuza kadar devam et
        # diskten cevap gelmesini bekle
        await disk(erisim_suresi)
        # diskten cevap geldi, gelen paketi
        # tampona at, ama once tampon dolu mu
        # kontrol et. Yoksa program akisi bloklanabilir
        while tampon.full():
            # tampon dolu, ses karti 1 paket tuketinceye
            # kadar bekle ve sonra tekrar dene
            await asyncio.sleep(0.1)
        
        # tampon bosaldi, 4kblik 1 paket at        
        await tampon.put(paket)

# ses karti modeli
async def sesk(paket, ses_karti_tazeleme):
    # gelen paketi burada tuket
    # paket bitinceye kadar bekleme yap
    await asyncio.sleep(ses_karti_tazeleme)
 
# ses kartina veri gonderme korosu
async def alici(tampon, veri_say, ses_karti_tazeleme):
    bos_paket = [0]*4000# dusen paket yerine konacak
    while True:# sonsuza kadar devam et
        # bir paket al ve gonder ama once tampon dolu mu bak
        while tampon.empty():
            # tampon bos 1 paket dusur
            veri_say["dusen_paket_sayisi"] +=1
            # toplam paket sayisini artir
            veri_say["toplam_paket_sayisi"] +=1
            # ses kartina bir bos paket gonder
            await sesk(bos_paket, ses_karti_tazeleme)
        
        # tampon dolu, bir paket al 
        veri_say["toplam_paket_sayisi"] +=1
        paket = await tampon.get()
        # ses kartina alinan paketi gonder
        await sesk(paket, ses_karti_tazeleme)

# asenkron monitor korosu 
# anlik raporlama yapar  
async def monitor(tampon, veri_say):
    tazeleme_hizi = 0.1#s
    i=0
    while True: # sonsuz dongu
        await asyncio.sleep(tazeleme_hizi)
        i+=tazeleme_hizi
        print(f"\rsaniye: {i:2.1f}:: %Doluluk: {tampon.qsize()*10:3}",
              f":: D.cerceve sayisi:{veri_say["dusen_paket_sayisi"]}",
              f":: T.cerceve sayisi: {veri_say["toplam_paket_sayisi"]}",
              end="")

# gorev iptal fonksiyonu
async def iptal(gorev):
    gorev.cancel()
    # iptal islemi de beklenmelidir
    try:
        await gorev
    except asyncio.CancelledError:# iptal istisnasi olustu
        pass# bos gec
    
# asenkron govde bolumu
async def ana():
    # tamponu temsil eden kuyruk olusturuluyor
    tampon             = asyncio.Queue(maxsize=10)
    erisim_suresi      = 0.01#s
    ses_karti_tazeleme = 0.1 #s
    # veri istatistiklerini tutan yapi
    veri_say           = {"dusen_paket_sayisi":0, "toplam_paket_sayisi":0}  
    
    print("BENZETIM BASLADI!")

    # gorevleri tanimliyoruz
    gorevler = []
    # monitor gorevi
    g = asyncio.create_task(monitor(tampon, veri_say))
    gorevler.append(g)#0
    # harddiskten veri getirme gorevi
    g = asyncio.create_task(verici(tampon, erisim_suresi))
    gorevler.append(g)#1
    # tamponun dolmasini bekliyoruz
    while not tampon.full():
        await asyncio.sleep(0.01)
    # ses kartina veri gonderme gorevi
    g = asyncio.create_task(alici(tampon, veri_say, ses_karti_tazeleme))
    gorevler.append(g)#2
    
    # belli bir zaman icin benzetimi surduruyoruz
    i=0
    while i<10:#sn
        await asyncio.sleep(1)
        i+=1
    # tam bu anda ses karti tarafindan tam 10 saniyelik veri(100 cerceve)
    # tuketilmis olmalidir. Ancak kayip zamandan dolayi asil deger
    # bundan farkli olmaktadir. Islem kaybindan kaynaklanan sure farki
    # %10 civarindadir.
    #print("::",i,".saniye ani")# 10. saniye anini kaydet 
    
    # gorevleri iptal etmeye basliyoruz
    # verici gorevi iptal ediliyor
    await iptal(gorevler[1])
    
    # alici gorevini iptal etmeden once
    # kuyruktaki tum elemenlar cekilinceye dek bekle
    
    #await asyncio.sleep(1)# sabit sure
    #await tampon.join()# kuyruk kirilmasindan dolayi duzgun calismiyor
    while not tampon.empty():
        await asyncio.sleep(0.1)

    # alici gorevi iptal ediliyor
    await iptal(gorevler[2])
    
    # kapatma gecikmesi, ekstra bir guncelleme yapilir
    await asyncio.sleep(0.1)

    # en son monitor gorevi iptal ediliyor
    await iptal(gorevler[0])
    
    print("\nBENZETIM DURDU!")
          
# ana program bolumu
if __name__ == '__main__':
    bas = time.perf_counter()
    asyncio.run(ana())
    bit = time.perf_counter()
    print(f"Toplam isletim suresi:{bit - bas : 2.3f} saniyedir.")