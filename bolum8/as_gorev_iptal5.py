# bu ornek bir dizi koronun wait() metodu kullanilarak
# isletim takibinin nasil yapilacagini gosterir.
# wait() metodu bir dizi gorevin beklenmesini belli bir
# sarta bagli olarak devam ettirir.
# buradaki kullanim seklinde gorevlerden birisinin sonlanmasi
# beklemeyi de sonlandirir (return_when=asyncio.FIRST_COMPLETED).

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
    # duruma gore asagidaki while
    # dongulerinden birini secin
    #while True: # sonsuz dongu
    while (i<10):# 10. saniyede sonlanir
        await asyncio.sleep(1)
        i+=1
        print(f"saniye: {i}")
    return f"{i}. saniyede saat durdu..."

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
    bekleyenler = (gorev1, gorev2, gorev3)
    
    # zaman korosu sonsuz dongude tutulursa
    # bu dongu hic bir zaman sonlanmaz
    # bu dongude bekleyenlerin deneme sayisini
    # takip ederek belli bir sinirdan sonra
    # sonlanmaya zorlayacak bir mekanizma kurulmalidir
    while bekleyenler:# bekleyen varsa devam et
        bitenler, bekleyenler = await asyncio.wait(
            bekleyenler,
            return_when=asyncio.FIRST_COMPLETED
        )# ilk tamamlanan gorevle birlikte bekleme biter
        # bitenlere atilan gorev sonucu ekrana yazdirilir
        cevap = bitenler.pop().result()
        print(f"sonuc: {cevap}")

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
