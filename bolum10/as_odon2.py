# bu ornek asenkron programlarda odon (olay dongusu) 
# ile manuel calismayi gosterir.
# once bir odon acilir ve ana koro bu odona atilir
# daha sonra bu odon sonsuza kadar calisacak sekilde
# isletime alinir ve kosturmaya baslanir
# ana koro bir baska koroyu mevcut odona atarak
# isletime sokar.
# isletime giren zaman() korosu 10 saniye sonra
# acik odonu durdurur
# durmanin akabinde acik odon kapatilir ve program sonlanir


# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# asenkron bir koro
async def zaman():
    # zamanlayici dongusu
    for i in range(10):# 10 saniye
        print(f"\rSaniye::{i}", end="")
        await asyncio.sleep(1)
    # mevcutta kosan odonu durdur
    # asagidaki satiri yorum satiri haline getirmekle
    # kapanis kontrolunu ana koroya verebiliriz
    # tum korolar tamamlanmadan odonu durdurmak
    # veya kapatmak dogru bir davranis degildir
    #asyncio.get_running_loop().stop()
    
# ana asenkron govde
async def ana():
    
    # Mevcut kosan odon sorgula
    odon = asyncio.get_running_loop()
    print(f"Ana koroda mevcut kosan odon: \n{odon}")
    
    # baslangic anini kaydet
    bas = time.perf_counter()
    # gorevleri baslatiyoruz
    #await asyncio.create_task(zaman())
    # manuel gorev olusturma ve odona atma
    await odon.create_task(zaman())
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"\nislem suresi:{bit-bas:2.3f} saniyedir")
    # mevcutta kosan odonu durduralim
    odon.stop()
    
# ana program bolumu
if __name__ == "__main__":
      
    # yeni bir odon ac
    odon = asyncio.new_event_loop()
    # acilan odonu mevcut odon yap
    asyncio.set_event_loop(odon)
    
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
        
    # ODON sorgula
    odon = asyncio.get_event_loop()
    print(f"Kapanis sonrasi ODON durumu: \n{odon}")
    