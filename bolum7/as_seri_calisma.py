# bu ornek korolarin seri (senkron) calismasini 
# gosterir

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# bir asenkron fonksiyon(koro) tanimi   
async def as_kup_al(sayi: int) -> int:
    print("kup alma islemi basladi!")
    # islem suresini temsil eden gecikme
    # korolarin asenkron islem yurutebilmesi
    # icin mutlak suretle asenkron yontemlerle
    # yazilmis alt rutinler kullanmasi gerekir
    # bu nedenle time kutuphanesinden cekilen
    # senkron uyku rutini yerine asenkron 
    # calismaya daha uygun hale getirilmis
    # versiyonunu asyncio kutuphanesinden
    # cekip kullaniyoruz. Ayrica, korolarin
    # asenkron kullanimi "await" deyimiyle
    # mumkun olur. "await" deyimi, ardindan gelen
    # koroyu isletime alir ve fakat hemen duraklatir
    # ta ki koro bir sonuc elde edinceye kadar
    # await deyiminin kullanimina sadece korolar
    # altinda musaade edilir. Normal fonksiyon tanimlarinda
    # veya ana program bolumunde kullanima musaade yoktur.
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
# asyncio.run() bir kez kullanilabildigi icin
# diger tum korolari bekledigimiz (await) bir
# ana govdeyi koro olarak tanimlamamiz gerekiyor
async def ana():
    # asenkron fonksiyonlarin (koro) senkron sirali cagrisi
    # ilk koro beklemesi
    kup = await as_kup_al(2)
    print()
    print(f"kup: {kup}")
    
    # ikinci koro beklemesi
    # ilk koro sonucunun gelmesi sarttir
    kare = await as_kare_al(kup)
    print()
    print(f"kare: {kare}")
    

# ana program bolumu
if __name__ == '__main__':
    
    # baslangic ani kaydediliyor
    print("ISLETIM BASLASIN!")
    bas = time.perf_counter()
    
    # ana korosunun isletilmesi
    cvp=asyncio.run(ana())
    
    # bitis ani kaydediliyor
    bit = time.perf_counter()
    print("ISLETIM TAMAMLANDI!")
    print(f"isletim suresi: { bit - bas : 2.3f}")
