# ipsiz calisan kronometre ornegi
# kronometre fonksiyonundaki sonsuz dongu 
# ancak programin kirilmasi (CTRL+C) ile durdurulabilir

# zamanlayici kutuphanesi
import time

# kronometre rutini
def kronometre():
    saniye = 0
    # sonsuz dongude sayım yapan blok
    while True:
        saniye = saniye + 1
        time.sleep(1)
        print(f"\r{saniye} saniye gecti...", end="")

# ana program blogu
kronometre()

# devam eden dongu dolayisiyla takip eden komut asla 
# isletim firsati bulamaz
input("Programdan cikmak icin Entere basiniz\n")
