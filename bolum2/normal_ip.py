# hayalet ozelligi kapali ip ornegi
# ip dahilinde sonsuz dongu oldugundan
# ip asla sonlanmadigi icin programi da
# sonlandirmak mumkun olmaz

# ip kutuphanesi
from threading import Thread
# zamanlayici kutuphanesi
import time

# kronometre ipi
def kronometre():
    saniye = 0
    # sonsuz dongude sayım yapan blok
    while True:
        saniye = saniye + 1
        time.sleep(1)
        print(f"\r{saniye} saniye gecti...", end="")

# ana program blogu
ip = Thread(target = kronometre)
ip.start()

# devam eden ip dolayisiyla ana program sonlansa da
# ekrana kronometre ipine ait mesaj cikmaya devam eder
input("Programdan cikmak icin Entere basiniz\n")
