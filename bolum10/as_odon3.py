# bu ornek asenkron programlarda odon (olay dongusu) 
# ile manuel calismayi gosterir.
# once bir odon acilir ve ana koro bu odona atilir
# daha sonra bu odon sonsuza kadar calisacak sekilde
# isletime alinir ve kosturmaya baslanir
# ana koro bir gericagrim fonksiyonunu isletilmek 
# uzere odona atar
# isletime giren zaman() fonksiyonu her 1 saniyede bir
# kendini geri cagirir. Bu dongu ana koronun 10 saniye
# sonra bir kapat olay nesnesini aktif hale getirmesi
# ile sonlanır.
# durmanin akabinde acik odon kapatilir ve program sonlanir


# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# zamanlayici gericagrim fonksiyonu
def zaman(i, odon):
    # kapatma sinyali aktif mi kontrol et
    if kapat.is_set():
        return# cagriyi bitir
    # zamanlayici dongusu
    print(f"\rSaniye:{i}", end="")
    # saniye sayacini ilerlet
    i+=1
    # kendine 1 saniye sonra isletilecek gericagrim yap
    # tikamasiz bir zamanlama odon tarafindan yurutulur
    # ancak zamanlama gorevinin tam olacagi garanti
    # edilemez. En az gecikme kadar beklenir, bekleme
    # daha uzun olabilir.
    odon.call_later(1, zaman, i, odon)
    # bu noktadan itibaren odonu mesgul edecek ve tikayacak
    # hic bir islemin olmamasi lazim. Aksi halde zamanlama
    # gorevi dogru calismayacaktir. asagidaki tikayici
    # uyku komutu bu durumu gostermek icin yorum satiri 
    # olmaktan cikarilmalidir
    #time.sleep(2)
      
# ana asenkron govde
async def ana():
    
    # Mevcut kosan odon sorgula
    odon = asyncio.get_running_loop()
    print(f"Ana koroda mevcut kosan odon: \n{odon}")
    
    # baslangic anini kaydet
    bas = time.perf_counter()
    # odon anini yazdiralim
    print(f"Mutlak Odon ani:{odon.time():.0f}")
    # zaman() gericagrim fonksiyonuna bir 
    # gericagrim yapiliyor. Geri cagrim odonda
    # gecikmesiz isleme alinir
    odon.call_soon(zaman, 0, odon)
    # 10 saniye bekle
    await asyncio.sleep(10)
    # gericagrimi iptal et
    print(f"\nSaat kapatiliyor! "
          f"\nMutlak Odon ani:{odon.time():.0f}")
    kapat.set()
    # 3 saniye daha bekle
    await asyncio.sleep(3)
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"\nislem suresi:{bit-bas:2.3f} saniyedir")
    # mevcutta kosan odonu durduralim
    odon.stop()
    
# ana program bolumu
if __name__ == "__main__":
    
    # zaman gericagrim fonksiyonunu kontrol icin
    # bir kapatma olayi tanimliyoruz
    kapat = asyncio.Event()
      
    # yeni bir odon ac
    odon = asyncio.new_event_loop()
        
    # mevcut odona bir koroyu at
    # isletim odonun isletime alinmasi ile gerceklesir
    odon.create_task(ana())
    
    # mevcut odonu kosturalim
    try:
        odon.run_forever()
    finally:# durdurma sonrasi program akisi buradan devam eder
        # kapatilma oncesinde odon durdurulmus olmalidir
        if odon.is_running():# odon kosuyor mu?
            # kosan odonu durduralim
            odon.stop()
        print("ODON kapaniyor...")
        # isletimde olan asenkron uretecler varsa once 
        # bunlar kapatilmalidir
        odon.run_until_complete(odon.shutdown_asyncgens())
        odon.close() # durdurma sonrasi odon kapatilir  
        