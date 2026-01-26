# bu ornek bir koronun iptal islemine
# karsi nasil korunacagini gosterir

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
    return sayi**3

# asenkron kare alma korosu   
async def as_kare_al(sayi: int) -> int:
    print("kare alma islemi basladi!")
    # islem suresini temsil eden gecikme
    await asyncio.sleep(2)# saniye bekle
    print("kare alma islemi tamamlandi!")
    return sayi**2

# asenkron zamanlama korosu   
async def zaman():
    i=0
    while True:
        await asyncio.sleep(1)
        i+=1
        print(f"saniye: {i}")

# asenkron govde bolumu
async def ana():
    # aktif olay dongusunu sorgulayip ekrana yazdiriyoruz
    odon = asyncio.get_running_loop()
    print(f"Aktif Olay dongusu: {odon}")
    
    # asenkron fonksiyonlarin (koro) paralel cagrisi
    # ilk koro gorevi
    gorev1 = asyncio.create_task(as_kup_al(2))
    
    # ikinci koro gorevi
    gorev2 = asyncio.create_task(as_kare_al(3))
    
    # zamanlayici gorevi
    gorev3 = asyncio.create_task(zaman())
    
    # simdi artik beklemeye haziriz.
    
    # birinci gorev bekleniyor
    kup = await gorev1
    print(f"kup: {kup}")
    
    # ikinci gorev bekleniyor
    kare = await gorev2
    print(f"kare: {kare}")
    
    # tum gorevler tamamlandigina gore zamanlayiciyi
    # iptal edebiliriz. Burada 3 saniyelik bir zamanasimi
    # belirliyoruz ancak gorevi iptale karsi koruyoruz
    try:
        await asyncio.wait_for(
              asyncio.shield(gorev3), timeout=3)
    except asyncio.TimeoutError:
        print("Zamanlayici gorevi beklenenden uzun surdu!")
    
    # 5 saniye daha bekliyoruz ve gorev program 
    # sonlanmasi nedeniyle otomatik iptal oluyor
    await asyncio.sleep(5)
    print("Program ve beraberindeki",
          "tum tamamlanmayan gorevler kapatiliyor...")

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
