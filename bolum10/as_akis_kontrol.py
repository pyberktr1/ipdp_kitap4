# asenkron bir olay kullanilarak bir koronun
# duraklatilmasi ve devam ettirilmesi suretiyle
# akisinin kontrol altina alinmasi
# bu teknikle gerceklesitirilen akis kontrolu
# bir kavsaktaki trafik lambasi misali korolarda
# senkron hareketi temin etmekte kullanilir.
# bu ornekte ikinci koronun, ilk koroda elde 
# edilen verilerle islem yaptigi varsayilmistir.
# bu nedenle once ilk koro sonra ikinci koro
# harekete gecirilmeli. Ayrica ilk koronun hareketi
# de ikinci koronun aldigi verilerle islemini 
# tamamlamasina baglidir. Bu nedenle herhangi bir anda
# sadece birisinin devamina musaade vardir.

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# duraklatilabilir/ devam ettirilebilir koro
async def dur_koro(kid, devam_et):
    print(f"{kid} goreve basladi!")
    # bir islem 3 kez tekrarlaniyor
    for i in range(3):
        # koro isletimini onay gelinceye kadar duraklat
        devam_et.clear()
        # olay set degilse bekle
        await devam_et.wait()
        # isletim musaadesi geldi
        print(f"{kid}::{i}. islemi gerceklestiriyor")
        # islem gecikmesi
        await asyncio.sleep(0.5)  
    print(f"{kid} gorevi tamamladi!")
        
# ana asenkron govde
async def ana():
    # duraklat/devam et olayi/sinyali
    devam_et1 = asyncio.Event()
    devam_et2 = asyncio.Event()
    
    # baslangic anini kaydet
    bas = time.perf_counter()
    
    # gorevler olusturuluyor
    g1=asyncio.create_task(dur_koro("koro1", devam_et1))
    g2=asyncio.create_task(dur_koro("koro2", devam_et2))
    # gorevlerin akisini kontrol et
    for _ in range(3):# 1 saniye aralikla dur/kalk yaptiriyoruz
        await asyncio.sleep(1)
        devam_et1.set()
        await asyncio.sleep(1)
        devam_et2.set()
    # gorevlerin sonlanmasini bekle
    await g1
    await g2
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"islem suresi:{bit-bas:2.3f}")
    
# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
    