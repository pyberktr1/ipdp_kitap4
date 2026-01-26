# bu ornek, asenkron dosya erisimi ile acilan bir dosyaya
# bir asenkron uretecte uretilen ve rastgele sayilardan olusan
# bir akisin (stream) nasil kaydedildigini gosterir. Uygulama orneginde
# ayni anda birden fazla dosya acilmaktadir ve ayni zamanli kayit 
# gerceklestirilmektedir.

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time
# asenkron dosya erisimi kutuphanesi
# "python3 -m pip install aiofiles" komutuyla kurulum gerektirir
import aiofiles
# rastgele sayi uretmek icin isletim sistemi kutuphanesi
import os

# programda kullanilan sabitler
# paket ebadi 
pebat = 4096 # (bayt)
# dosya basina paket sayisi 
psayi = 1000 # (adet)
# ayni zamanli acilan dosya sayisi
dsayi = 5 #(adet)

# rastgele sayilari pebat baytlik paketler halinde ureten
# asenkron uretec korosu
async def auretec():
    while True:
        # pebat baytlik rastgele bayt deger
        yield os.urandom(pebat)

# asenkron uretecten gelen akisi dosyaya yazan
# asenkron dosya korosu
async def adosya(dosya):
    au = auretec()# asenkron uretec nesnesi
    # asenkron uretecten paket cek ve dosyaya yaz
    async with aiofiles.open(dosya, mode="wb") as d:
        i=0# paket sayaci
        # paketleri getir
        async for paket in au:
            # gelen paketi dosyaya yazmayi bekle
            await d.write(paket)            
            i+=1# paket sayacini ilerlet
            if i>=psayi:# psayi. pakette dur
                break
    
# ana asenkron govde
async def ana():
    print("Dosyaya yazma islemi basliyor...")
    # baslangic anini kaydet
    bas = time.perf_counter()
    # gorevleri baslatiyoruz ve bekliyoruz
    g = await asyncio.gather( *(adosya(f".\\dosyalar\\dosya{i}.rnd") 
                                  for i in range(dsayi)), 
                              return_exceptions=True )
    # bitis anini kaydet
    bit = time.perf_counter()
    print("Dosyaya yazma islemi tamamlandi!")
    print("Yazma islemi sonuclari")
    print(g)
    print(f"\nislem suresi:{bit-bas:2.3f} saniyedir")
    
# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
    