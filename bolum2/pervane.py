# hayalet ozelligi acik ip ile donen kursor

# ip kutuphanesi
from threading import Thread
# zamanlayici kutuphanesi
import time

# pervane ipi
def pervane():
    p_simge = ["|","/","-","\\"]
    # sonsuz dongu
    while True:
        for p in p_simge:
            time.sleep(0.1)
            print(f"{p}\b", end="", flush=True)
        
# ana program blogu
ip = Thread(target = pervane, daemon = True)
ip.start()

# Entere basilmasi ile birlikte ana program ve hayalet ip 
# isletimi tamamen durdurulur.
input("Programdan cikmak icin Entere basiniz...")
