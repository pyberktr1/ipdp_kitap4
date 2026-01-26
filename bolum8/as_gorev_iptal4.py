# bu ornek bir koronun bir dizi zamanasimi
# sonrasinda nasil kapanmaya zorlanacagini gosterir

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
    while True: # sonsuz dongu
    #while (i<10):# 10. saniyede sonlanir
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
    
    # birinci gorev bekleniyor
    kup = await gorev1
    print(f"kup: {kup}")
    
    # ikinci gorev bekleniyor
    kare = await gorev2
    print(f"kare: {kare}")
    
    # tum gorevler tamamlandigina gore zamanlayiciyi
    # iptal edebiliriz. Burada 3 saniyelik bir zamanasimi
    # belirliyoruz ancak gorevi iptale karsi koruyoruz.
    # Zamanasimi sayisi max_deneme degerine ulastiginda
    # gorev hala kendi rizasiyla kapanmamissa kapanmaya
    # zorluyoruz
    MAX_DENEME = 3    # deneme sayisi limiti
    zm_as      = True # zaman asimi durumu
    n_deneme   = 0    # deneme sayisi
    # zamanasimi varsa ve max deneme sayisina ulasilmadiysa
    # tekrar dene
    cvp   = None # islem sonucu
    zm_as = True # zaman asimi sinyali
    while (zm_as and (n_deneme < MAX_DENEME)):
        # gorev3 bekleniyor
        try:
            cvp = await asyncio.wait_for(asyncio.shield(gorev3), 
                                            timeout=3)
            zm_as = False # zaman asimi olmadan gorev sonlandi
        except TimeoutError:
            print("Zamanlayici gorevi beklenenden uzun surdu!")
            n_deneme+=1# deneme sayisini ilerlet
            print(f"Deneme sayisi: {n_deneme}")
    # dongu zaman asimi ile sonuclandi ise deneme sayisi siniri
    # asilmis demektir. Aksi halde gorev normal bicimde sonlanmistir    
    if zm_as:# deneme siniri asildi mi?
        print("Max. deneme sayisina ulasildi.",
              " Gorev kapanmaya zorlanacak!")
        if not gorev3.done():
            print('Zamanlayici iptal ediliyor...')
            gorev3.cancel()
    else:
        print(f"Gorev normal bir sekilde sonlandi. Sonuc :{cvp}")

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
