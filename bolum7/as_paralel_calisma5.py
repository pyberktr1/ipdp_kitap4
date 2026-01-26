# bu ornek korolarin paralel (asenkron) calismasi
# esnasinda gorevlerin sonuclarini tamamlanma
# sirasina gore sunmayi gosterir

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
    return ["kup", sayi**3]

# bir baska asenkron fonksiyon(koro) tanimi   
async def as_kare_al(sayi: int) -> int:
    print("kare alma islemi basladi!")
    # islem suresini temsil eden gecikme
    await asyncio.sleep(2)# saniye bekle
    print("kare alma islemi tamamlandi!")
    return ["kare", sayi**2]

# asenkron govde bolumu
async def ana():
    # asenkron fonksiyonlarin (koro) paralel cagrisi
    # sonuclar sounclanma sirasina gore sunulur
    for gorev in asyncio.as_completed([as_kup_al(2), as_kare_al(3)]):
        sonuc = await gorev
        print(f"{sonuc[0]}: {sonuc[1]}")    
    
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
