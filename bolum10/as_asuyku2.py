# Bu ornek asyncio.sleep() metodunun nasil calistigini gosteren
# esdeger bir asuyku() korosunu ve kullanimini gosterir.
# parametrede verilen saniye kadar asenkron uyku gerceklesir.
# uygulamanin bu versiyonunda mesgul edici gorev icinde
# uyku gorevini aksatmayi engelleyecek bir tedbir alinmistir.

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
        # her 1000 sayimda bir fasila veriyor 
        # ve kontrolu odona devrediyoruz
        # boylece asuyku() gorevi de isletme
        # icin bir fırsat elde ediyor.
        if i%10**3 == 0:
            await odon_yinele()
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
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"gorev() sonrasi islem suresi:{bit-bas:2.3f}")

# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
        
