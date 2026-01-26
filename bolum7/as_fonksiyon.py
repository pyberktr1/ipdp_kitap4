# bu ornek senkron ve asenkron fonksiyon 
# (yardimci rutin - coroutine veya kisaca koro)
# arasindaki farklari ve koro isletimini gosterir

# asenkron g/c kutuphanesi 
import asyncio

# normal (senkron) bir fonksiyon tanimi
def kup_al(sayi: int) -> int:
    # sayinin kupunu dondur
    return sayi**3

# yukaridaki senkron fonksiyon ile ayni isi yapan
# asenkron fonksiyon(koro) tanimi   
async def as_kup_al(sayi: int) -> int:
    return sayi**3

# ana program bolumu
if __name__ == '__main__':
    # senkron fonksiyon cagrisi
    cvp=kup_al(2)
    print(f"senkron cevap: {cvp}")
    print()
    
    # dogrudan asenkron fonksiyon cagrisi, 
    # bir koro nesnesi dondurur
    cvp=as_kup_al(2)
    print(f"koro nesnesi: {cvp}")
    
    # gercek asenkron fonksiyon cagrisi
    # asyncio.run() sadece korolar icin ve
    # sadece bir kez kullanilabilir
    cvp=asyncio.run(as_kup_al(2))
    print()
    print(f"asenkron cevap: {cvp}")
        
