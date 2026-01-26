# bu ornek korolarin paralel (asenkron) calismasini 
# gosterir

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# bir asenkron fonksiyon(koro) tanimi   
async def as_kup_al(sayi: int) -> int:
    print("kup alma islemi basladi!")
    # islem suresini temsil eden gecikme
    await asyncio.sleep(3)# saniye bekle
    print("kup alma islemi tamamlandi!")
    return sayi**3

# bir baska asenkron fonksiyon(koro) tanimi   
async def as_kare_al(sayi: int) -> int:
    print("kare alma islemi basladi!")
    # islem suresini temsil eden gecikme
    await asyncio.sleep(2)# saniye bekle
    print("kare alma islemi tamamlandi!")
    return sayi**2

# asenkron govde bolumu
async def ana():
    # asenkron fonksiyonlarin (koro) paralel cagrisi
    # bunun icin koro nesnelerini gorev haline getirip
    # olay dongusune (event loop) atariz. Bu nedenle 
    # korolarda bekleme (await) yapmayacagiz.
    # paralel calismayi temin edebilmek icin iki koronun
    # birbirinden bagimsiz calismasi gerekir
    # bu nedenle her bir koroyu farkli veri girdileri ile
    # isletecegiz.
    # ilk koro gorevi
    gorev1 = asyncio.create_task(as_kup_al(2))
    
    # ikinci koro gorevi
    gorev2 = asyncio.create_task(as_kare_al(3))
    
    # simdi artik beklemeye haziriz.
    # bekleme islemini koro yerine o koronun atandigi
    # gorev uzerinden yapacagiz. Boylece olay dongusu
    # bizim yerimize beklemeleri yoneterek her iki koronun
    # ayni zamanli isletimini saglayacak.
    # bu islemde kullanilacak olay dongusu run() deyimi ile
    # ana program bolumunde gerceklestirilir. Ayni anda birden
    # fazla olay dongusunun bir arada isletimi onerilmez. 
    # Sadece tek olay dongusu uzerinden ayni zamanli isletim 
    # gerceklestirilir. Birden fazla olay dongusunun birarada
    # kullanilmaya calisilmasi cesitli sorunlara neden olur.
    
    # birinci gorev bekleniyor
    kup = await gorev1
    print(f"kup: {kup}")
    
    # ikinci gorev bekleniyor
    kare = await gorev2
    print(f"kare: {kare}")
    
    # hangi gorev once sonlanirsa onun tamamlanma mesaji hemen ekrana gelir
    # burada bir sira gozetmek mumkun olmaz. Fakat await deyimlerinin dikte
    # ettigi bekleme sirasi dolasiyla sonuclar ekrana sirali (once kup sonra
    # kare sonucu) gelir. Kare islemi once tamamlansa da sonucu kupten sonra
    # yazdirilir.
    

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
