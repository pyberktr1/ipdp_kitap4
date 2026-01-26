# ip islemlerinin Thread sinifi uzerinden gerceklestirilmesi
# bu ornek dosyaya yazma islemini Thread sinifi uzerinden
# gerceklestirir
# ip islemleri icin kutuphane
from threading import Thread

# ip sinifi yeniden duzenleniyor
# dosyaya yazma gerceklestiren yeni bir ip sinifi olusturuluyor
class ip_dosya_yaz(Thread):
    # baslatma blogu
    def __init__(self, d_ad: str, satir:str) -> None:
        super().__init__()
        self.d_ad  = d_ad    # yazilacak dosya adi
        self.satir = satir   # yazilacak satir verisi
    # isletme blogu
    def run(self) -> None:
        print(f"{self.d_ad} yazdiriliyor...\n", end="")
        with open(self.d_ad, 'a') as d:
            d.write(self.satir)

# ana program blogu
def ana() -> None:
    # yazdirma islem verisi
    veri = [
        ["./dosya/metin1.txt", "SAKLA SAMANI\n"],
        ["./dosya/metin2.txt", "GELIR ZAMANI\n"]
    ]
    
    # ipler tanimlaniyor
    ipler = [ip_dosya_yaz(d_ad, satir) for [d_ad, satir] in veri]
    # ipler baslatiliyor
    [ip.start() for ip in ipler]
    # iplerin tamamlanmasi bekleniyor
    [ip.join() for ip in ipler]

    print("Tüm islemler tamamlandi!")

# ana program blogu __main__ ad alanından cagriliyor
if __name__ == "__main__":
    ana()
    
