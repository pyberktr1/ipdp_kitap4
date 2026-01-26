# bu ornek bir koro grubunun bir iptal gorevi kullanilarak
# nasil iptal edilebilecegini gosterir.

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# asenkron kup alma korosu  
async def as_kup_al(sayi: int) -> int:
    print("kup alma islemi basladi!")
    # islem suresini temsil eden gecikme
    await asyncio.sleep(3)# saniye bekle
    print("kup alma islemi tamamlandi!")
    sonuc = sayi**3
    print(f"kup: {sonuc}")
    

# asenkron kare alma korosu   
async def as_kare_al(sayi: int) -> int:
    print("kare alma islemi basladi!")
    # islem suresini temsil eden gecikme
    await asyncio.sleep(2)# saniye bekle
    print("kare alma islemi tamamlandi!")
    sonuc = sayi**2
    print(f"kare: {sonuc}")

# asenkron zamanlama korosu   
async def zaman():
    i=0
    # duruma gore asagidaki while
    # dongulerinden birini secin
    while True: # sonsuz dongu
    #while (i<10):# 10. saniyede sonlanir
        await asyncio.sleep(1)
        i+=1
        print(f"saniye: {i}")
    print(f"{i}. saniyede saat durdu...")

# gorev grubunu sonlandirmakta kullanilacak istisna sinifi tanimi
class GorevGrubunuSonlandir(Exception):
    """gorev grubunu sonlandirma istisnasi"""

# gorev grubunu sonlandirmaya zorlayacak ozel koro tanimi
async def gorev_grubunu_sonlandir():
    # bu koro cagrisi ile birlikte bir istisna uretilir
    raise GorevGrubunuSonlandir()

# asenkron govde bolumu
async def ana():
    # aktif olay dongusunu sorgulayip ekrana yazdiriyoruz
    odon = asyncio.get_running_loop()
    print(f"Aktif Olay dongusu: {odon}")
    
    # asenkron fonksiyonlarin (koro) paralel cagrisi
    # tum korolari bir gorev grubu (gg) altinda birlestiriyoruz
    try:
        async with asyncio.TaskGroup() as gg:
            # normal gorevler gruba atiliyor
            gg.create_task(as_kup_al(2))
            gg.create_task(as_kare_al(3))
            gg.create_task(zaman())
            # gorevlerin tamamlanmasi icin bir sure veriyoruz
            await asyncio.sleep(12)# saniye
            # gorev grubunu sonlanmaya zorlayacak gorevi gruba 
            # atiyoruz. Uretilen istisna grubu kapanmaya zorlar
            gg.create_task(gorev_grubunu_sonlandir())
    # asenkron gorevlerde ayni anda meydana gelebilecek bir dizi
    # istisnayi saglikli bicimde isleyebilmek icin except deyiminden
    # sonra yildiz koyarak bu durumu ifade etmemiz gerekir.
    except* GorevGrubunuSonlandir:# bir istisna grubu var
        print("Tum gorevler durdu!")

# ana program bolumu
if __name__ == '__main__':
    
    # baslangic ani kaydediliyor
    print("ISLETIM BASLASIN!")
    bas = time.perf_counter()
    
    # ana korosunun isletilmesi
    # butun korolar birarada calisir
    asyncio.run(ana())
    
    # bitis ani kaydediliyor
    bit = time.perf_counter()
    # korolar ayni zamanli isletildigi icin
    # islem sonucu daha kisa surede elde edilir
    print("ISLETIM TAMAMLANDI!")
    print(f"isletim suresi: { bit - bas : 2.3f}")
