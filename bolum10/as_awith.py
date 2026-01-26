# bu ornek asenkron korolarda asenkron with deyimi ile
# asenkron web tarama oturumunun nasil bir baglamda (context)
# yonetilebilecegini gosterir

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time
# asenkron web kutuphanesi
# "python3 -m pip install aiohttp" komutuyla kurulum gerektirir
import aiohttp

# web durum sorgulamasini yapan koro
async def web_durum(web):
    # once musteri oturumunu aciyoruz
    async with aiohttp.ClientSession() as oturum:
        # sonra acilmis oturum araciligi ile web sorgulamasi
        # yapiyor ve sonucu donduruyoruz.
        async with oturum.get(web) as sonuc:
            return f"{web} adresi icin durum: {sonuc.status}"
    
# ana asenkron govde
async def ana():
    # web adresleri tanimlaniyor
    webler = [
                # normal adresler icin "200:durum normal" kodu uretilir
                "http://www.sm0vpo.com/rx/tda7k-rx2.htm",
                "http://www.sm0vpo.com/rx/tba120-1.htm",
                "http://www.sm0vpo.com/rx/tda7000.htm",
                "http://www.sm0vpo.com/rx/quickrx.htm",
                "http://www.sm0vpo.com/rx/synth.htm",
                "http://www.elektormagazine.com/",
                # "404:sayfa bulunamadi" kodu uretilir
                "http://www.sm0vpo.com/rx/books.html",
                # siteye baglanma hatasi uretilir
                # hatali link adresi
                "http://www.elektormagazin.com/"
                
                ]
    print("\nWeb adresleri durum bilgisi sorgulaniyor...")
    # baslangic anini kaydet
    bas = time.perf_counter()
    # gorevleri baslatiyoruz ve bekliyoruz
    g = await asyncio.gather(*(web_durum(web) for web in webler), return_exceptions=True)
    # sonuclar raporlaniyor
    for msg in g:
        print(msg)
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"\nislem suresi:{bit-bas:2.3f} saniyedir")
    
# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
    