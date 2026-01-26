# Bu ornek asyncio.sleep() metodunun nasil calistigini gosteren
# esdeger bir asuyku() korosunu ve kullanimini gosterir.
# parametrede verilen saniye kadar asenkron uyku gerceklesir.
# uykuda gecen sure en az verilen saniye kadardir.
# gercekte odon dongu tepki suresi ile alakali olarak
# daha uzun bir deger olabilecegi icin hassas zamanlama gorevleri
# icin onerilmez. Bu durum asyncio.sleep() icin de aynen gecerlidir.

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# olay dongusune (odon) kontrolu devretmeyi saglayan sinif
class odon_yinele:
    def __await__(self):
        yield# akisi duraklat ve kontrolu devret

# asyncio.sleep() metoduyla ayni gorevi goren
# asuyku() korosu
async def asuyku(s:float):
    # uyanis anini hesapla
    uyan = time.time() + s # saniye
    while True:# sonsuz donguye gir
        # uyanma vakti geldi mi?
        if time.time() >= uyan:
            return# gorevi bitir
        else:# uyanmaya daha var 
            # kontrolu olay dongusune devret
            # uyanis aninin tekrar kontrolu
            # odon bir sonraki kontrol devrinde
            # gerceklesir.
            await odon_yinele()

# odonu asiri mesgul edecek bir asenkron gorev 
async def gorev():
    p=0
    for i in range(10**9):
        p+=1
    print("gorev tamamlandi!")
    
# ana asenkron govde
async def ana():
    print("tum gorevler baslasin!")
    # baslangic anini kaydet
    bas = time.perf_counter()
    # olay dongusunu yukleyecek bir gorev baslatiyoruz
    g=asyncio.create_task(gorev())
    # uyku gorevini baslatiyoruz
    #await asyncio.sleep(2)
    await asuyku(2)
    
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"islem suresi:{bit-bas:2.3f}")
    await g
    
# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
        
