# bu ornek asenkron programlarda odon (olay dongusu) 
# ile calismayi gosterir

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
        
# ana asenkron govde
async def ana():
    
    # Mevcut kosan odon sorgula
    odon = asyncio.get_running_loop()
    print(f"Ana koroda mevcut kosan odon: \n{odon}")
    
    # baslangic anini kaydet
    bas = time.perf_counter()
    # gorevleri baslatiyoruz
    await asyncio.create_task(zaman())
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"\nislem suresi:{bit-bas:2.3f} saniyedir")
    
# ana program bolumu
if __name__ == "__main__":
    
    # ODON sorgula, normal isletim icin alttaki iki satırı
    # yorum satırı haline getiriniz
    #odon = asyncio.get_event_loop()
    #print(f"Acilis oncesi ODON durumu: \n{odon}")
    
    # yeni bir odon ac
    odon = asyncio.new_event_loop()
    # acilan odonu mevcut odon yap
    asyncio.set_event_loop(odon)
    
    # ODON sorgula
    odon = asyncio.get_event_loop()
    print(f"Acilis sonrasi ODON durumu: \n{odon}")
    
    # mevcut odona bir koroyu atmak suretiyle islet
    # koro tamamlanciya kadar odon acik kalir
    # sonra kapatilir
    odon.run_until_complete(ana())

    # ODON sorgula
    odon = asyncio.get_event_loop()
    print(f"Ana koro sonrasi ODON durumu: \n{odon}")
    