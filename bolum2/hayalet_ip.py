# hayalet ozelligi acik ip ornegi
# ip dahilinde sonsuz dongu oldugundan
# ip asla sonlanmaz 
# ancak ana programin bitmesi ile tum
# hayalet ipler de otomatik sonlandigindan
# artik ekrana mesaj gelmez
# boylece sondaki input komutunun fonksiyonunu
# tam olarak gorebiliriz.

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
ip = Thread(target = kronometre, daemon = True)
ip.start()

# Entere basilmasi ile birlikte ana program ve hayalet ip 
# isletimi tamamen durdurulur.
input("\nProgramdan cikmak icin Entere basiniz... \033[F")
