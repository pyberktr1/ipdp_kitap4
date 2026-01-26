# bu ornek asenkron korolarda senkron for donguleri
# kullanimini gosterir

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# yinelenebilir veri fonksiyonu
# senkron uretec
def yinele():
    i=0# baslangic degeri
    while i<10:# 9'a kadar say
        # islem gecikmesi
        time.sleep(0.5)        
        yield i# yinelemede dondurulecek deger
        i+=1# degeri degistir

# senkron for dongusu kullanan koro
async def for_dongu(fid):
    # senkron for dongusu ile yineleyerek gezme
    # yinelenecek veri kalmadiginda otomatik durur
    for i in yinele():
        print(f"{fid}::{i}")
        
# ana asenkron govde
async def ana():
    # baslangic anini kaydet
    bas = time.perf_counter()
    # gorevleri baslatiyoruz
    g = await asyncio.gather(*(for_dongu(i) for i in range(2)))
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"islem suresi:{bit-bas:2.3f}")
    
# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
    