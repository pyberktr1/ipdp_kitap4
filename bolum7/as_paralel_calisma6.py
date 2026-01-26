# bu ornek bir koroda uretilen orneklerin bir 
# asenkron for dongusu araciligi ile nasil 
# cekilebilecegini gosterir

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time
# rastgele sayi uretici
import random

# bir asenkron uretec koro tanimi   
async def uretec():
    ornek_no = 0 # ornek numarasi
    while True:# sonsuz dongude uretim
        # ornek uretim gecikmesi
        ornek_no+=1# bir sonraki ornek
        await asyncio.sleep(0.5)
        # ornek uretiliyor
        ornek = [ornek_no, random.uniform(0, 10)]
        yield ornek # talep durumunda ornegi gonder
        
# asenkron zamanlama korosu   
async def zaman():
    i=0
    while True:
        await asyncio.sleep(1)
        i+=1
        print(f"saniye: {i}")

# asenkron govde bolumu
async def ana():
    # asenkron fonksiyonlarin (koro) paralel cagrisi
    asyncio.create_task(zaman())# zamanlama gorevi isletilir
    # uretecten ornekler bir asenkron for dongusu ile cekilir
    async for ornek in uretec():
        print(f"ornek no{ornek[0]}= {ornek[1]:2.3f}")
        # 11. ornekte donguyu sonlandir
        if ornek[0]>10:
            print("ornekleme islemi sonlandi!")
            break
     
# ana program bolumu
if __name__ == '__main__':
    
    # baslangic ani kaydediliyor
    print("ISLETIM BASLASIN!")
    bas = time.perf_counter()
    
    # ana korosunun isletilmesi
    # butun korolar birarada calisir
    cvp = asyncio.run(ana())
    
    # bitis ani kaydediliyor
    bit = time.perf_counter()
    # korolar ayni zamanli isletildigi icin
    # islem sonucu daha kisa surede elde edilir
    print("ISLETIM TAMAMLANDI!")
    print(f"isletim suresi: { bit - bas : 2.3f}")
