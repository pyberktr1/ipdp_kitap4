# bu ornek bir asenkron for dongusu ile asenkron bir yinelenbilir
# korodan veri cekilmesini gosterir. 

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# yinelenebilir veri korosu
# asenkron uretec
async def yinele():
    i=0# baslangic degeri
    while i<10:# 9'a kadar say
        # islem gecikmesi
        await asyncio.sleep(0.5)        
        yield i# yinelemede dondurulecek deger
        i+=1# degeri degistir

# asenkron for dongusu kullanan koro
async def afor_dongu(fid):
    # asenkron for dongusu ile yineleyerek gezme
    # yinelenecek veri kalmadiginda otomatik durur
    async for i in yinele():
        print(f"{fid}::{i}")
        
# ana asenkron govde
async def ana():
    # baslangic anini kaydet
    bas = time.perf_counter()
    # gorevleri baslatiyoruz
    g = await asyncio.gather(*(afor_dongu(i) for i in range(2)))
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"islem suresi:{bit-bas:2.3f}")
    
# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
    