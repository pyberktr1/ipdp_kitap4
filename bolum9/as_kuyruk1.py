# Bu ornek kollektif calisma gosteren bir dizi tas kirma unitesi
# modeli uzerinden asenkron yapilarda kuyruk kullanimini gosterir.
# Bir dizi tas kirma unitesi (tuketici) tek bir besleyici (uretici)
# ile kuyruk uzerinden beslenir. Her bir tas kirma unitesi saniyede
# 1 kg tas ogutebilmektedir. Bu durumda 4 unite 1 saniyede 4 kg ogutur.

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time
# rastgele deger ureteci
import random

# kirilan toplam tas sayaci
toplam_tas = 0#kg

# tas besleme unitesi modeli korosu
async def tas_besleme(besleme):
    global toplam_tas 
    for _ in range(36):# 36 adet tas uret ve at
        tas = random.uniform(0.5, 1.5)#kg
        toplam_tas += tas# toplam uretimi kaydet
        # beslemeye at ve bekle. Kuyruk sonsuz oldugundan hic
        # bir zaman dolmaz ve dolayisiyla bekleme yasanmaz.
        # ancak kuyruga bir sinir konuldugunda bu bolumde blokaj
        # olur ve program ilerlemez. tas_kirici() korosunda çekim
        # oldugu muddetce sorun yasanmaz
        await besleme.put(tas) 
        # islem gecikmesi
        await asyncio.sleep(random.uniform(0.1,0.2))
        
    # besleme tamam
    print("Uretici: besleme tamamlandi!")
    
# tas kirma unitesi modeli korosu
async def tas_kirici(no, besleme):
    while True:# sonsuza kadar devam et
        # beslemeden yeni bir tas al
        tas = await besleme.get()

        # Tasin ogutulmesini bekle (1kg=1s, 2kg=2s)
        await asyncio.sleep(tas)

        # tas ogutumunun tamamlandigini bildir.
        besleme.task_done()

        print(f"Tas kirici{no}, {tas:2.3f} kg tas oguttu")

# asenkron govde bolumu
async def ana():
    # global degisken tanimi
    global toplam_tas
    
    # besleme mekanizmasini temsil eden kuyruk olusturuluyor
    besleme = asyncio.Queue()#maxsize=1)
    
    # Beslemedeki tum taslarin ogutulumesini bekliyoruz
    bas = time.perf_counter()# baslangic anini kaydet

    
    # Rastgele kiloda taslar uretiliyor ve beslemeye atiliyor
    tas_besle = asyncio.create_task(tas_besleme(besleme))
    
    # 4 adet tas kirici uniteyi ayri birer gorev halinde tanimliyoruz
    tas_kiricilar = []
    for i in range(4):
        tas_kirma = asyncio.create_task(tas_kirici(i, besleme))
        tas_kiricilar.append(tas_kirma)
     
    # tum gorevlerin baslamasi icin bir sure bekliyoruz
    await asyncio.sleep(1)
    
    # kuyruktaki tum elemenlar cekilinceye dek bekle
    await besleme.join() 
    
    # bitis anini kaydet
    bit = time.perf_counter()

    # Sonsuz dongu icerdigi icin tas kiricilari durduruyoruz
    for tas_kirma in tas_kiricilar:
        tas_kirma.cancel()
        
    # Tas kiricilar hemen durmaz, o yuzden hepsinin durdugundan emin oluyoruz
    # halihazirda durmus gorevler "CancelledError" istisnasi ureteceginden
    # bu istisnalari susturmak icin "return_exceptions" parametresi set
    # edilmelidir.
    await asyncio.gather(*tas_kiricilar, return_exceptions=True)

    print(f"4 tas kirici {bit - bas:2.3f} saniyede,",
          f"\ntoplam {toplam_tas:2.3f} kg tas oguttu")
          
# ana program bolumu
if __name__ == '__main__':
    asyncio.run(ana())