# ip islemlerinin Thread sinifi uzerinden gerceklestirilmesi
# bu ornek dosyadan okuma islemini Thread sinifi uzerinden
# gerceklestirir
# ip islemleri icin kutuphane
from threading import Thread

# ip sinifi yeniden duzenleniyor
# dosyadan okuma gerceklestiren yeni bir ip sinifi olusturuluyor
class ip_dosya_oku(Thread):
    def __init__(self, d_ad: str) -> None:
        super().__init__()
        self.d_ad = d_ad                        # okunacak dosya adi
        self.durum = "Dosyadan okuma basarili"  # dosya okuma durumu
        self.satir = ""                         # dosyadan okunan veri

    def run(self) -> None:
        print(f"{self.d_ad} dosyasindan okuma yapiliyor...\n", end="")
        try:
            with open(self.d_ad, 'r') as d:
                self.satir = d.read()
        except FileNotFoundError as hata:
            self.durum = f"Hata!: {self.d_ad} bulunamadi"
        except IOError as hata:
            self.durum = f"Hata!: {self.ad} I/O hatasi"

# Ana program blogu
def ana() -> None:
    dosyalar = [
        "./dosya/metin1.txt",
        "./dosya/metin2.txt"
    ]

    # ipler olusturuluyor
    ipler = [ip_dosya_oku(d_ad) for d_ad in dosyalar]

    # ipler baslatiliyor
    [ip.start() for ip in ipler]

    # iplerdeki islemlerin bitmesini bekle
    [ip.join() for ip in ipler]

    # her bir dosya icerigi ve durumunu ekrana listele
    [print(f"{ip.d_ad} : \n{ip.satir} :: dosya durumu: {ip.durum}") for ip in ipler]

# ana program blogu cagriliyor
if __name__ == '__main__':
    ana()
