# bu ornek asenkron korolarda yinelenebilir bir korodan
# anext deyimi kullanilarak nasil veri cekilecegini
# gosterir

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# yinelenebilir veri korosu
async def yinele():
    i=0# baslangic degeri
    while i<10:# 9'a kadar say
        # islem gecikmesi
        await asyncio.sleep(0.5)        
        yield i# yinelemede dondurulecek deger
        i+=1# degeri degistir

# anext deyimiyle yineleme yaparak bir yinelenebilir
# korodan veri cekecek olan koro
async def anext_dongu(fid):
    # anext ile veri cekmek
    # yineleme ile veri cekilecek koro nesnesi
    y = yinele() 
    # sonsuz dongu kurulur
    # yinelencek veri kalmadiginda "StopAsyncIteration"
    # istisnasi donguyu kirmakta kullanilir
    while True:
        try:# istisna gozleme
            # bir sonraki veriyi cek (yineleme yap)
            i = await anext(y)# yineleme bekleniyor
            print(f"{fid}::{i}")
        except StopAsyncIteration:# yinelenecek veri kalmadi
            break
        
# ana asenkron govde
async def ana():
    # baslangic anini kaydet
    bas = time.perf_counter()
    # gorevleri baslatiyoruz
    g = await asyncio.gather(*(anext_dongu(i) for i in range(2)))
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"islem suresi:{bit-bas:2.3f}")
    
# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
    