# bu ornek geleceklerin (future) nasil calistigini gosterir

# asenkron g/c kutuphanesi 
import asyncio
# zamanlayici kutuphanesi
import time

# gelecegi set edecek gorev
async def gorev(gelecek):
    # 3 saniye gecikme
    await asyncio.sleep(3)
    gelecek.set_result("GELECEK SIMDI") 

# ana asenkron govde
async def ana():
    # beklemek icin bir gelecek olusturuyoruz
    gelecek = asyncio.Future()
    # gelecegin belli bir gecikmeden sonra
    # set edilmesini saglayacak bir gorevi
    # odona atiyoruz
    g=asyncio.create_task(gorev(gelecek))

    print("gelecek bekleniyor!")
    # baslangic anini kaydet
    bas = time.perf_counter()
    # gelecegi bekliyoruz. Gelecek set edilmeden 
    # beklemeden cikilmaz
    cvp = await gelecek
    # bitis anini kaydet
    bit = time.perf_counter()
    print(f"gelecek sonucu : {cvp}")
    print(f"islem suresi:{bit-bas:2.3f}")
    # gorevin bitmesi bekleniyor
    await g
    
# ana program bolumu
if __name__ == "__main__":
    asyncio.run(ana())
        
