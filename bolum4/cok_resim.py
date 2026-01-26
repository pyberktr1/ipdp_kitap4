# Bu ornek coklu proseste resimleri paralel bicimde isleyen
# bir resim isleme prosesini gosterir

# zamanlayici kutuphanesi
from time import perf_counter
# isletim sistemi fonksiyonlari
import os
# resim isleme kutuphanesi
from PIL import Image as Resim, ImageFilter as ResFiltre
# coklu proses kutuphanesi
import multiprocessing as mp

# resim dosyalari
resimler = [
    "./resim/1.jpg",
    "./resim/2.jpg",
    "./resim/3.jpg",
    "./resim/4.jpg",
    "./resim/5.jpg",
]

# resim isleme fonksiyonu
def resim_isle(resim, islem_yeri ='islem'):
    # resim dosyasini acalim
    res = Resim.open(resim)
    
    # Gaussian blur filtresini uygulayarak
    # yeni bir yere atalim
    res_filtre = res.filter(ResFiltre.GaussianBlur(16))

    # Filtrelenmis resmi dikey eksende aynalayalim
    res_filtre_ayna = res_filtre.transpose(method=Resim.FLIP_TOP_BOTTOM)
    
    # yeni bir resim olusturarak orjinal ve islenmis resmi monte edelim
    # once resim ebadini alalim
    (x, y) = res.size
    
    # dikeyde iki kat yatayda bir kat ebatli yeni resim alani olusturuluyor
    yeni = Resim.new('RGB', (x, 2*y), (250,250,250))
    
    # resimleri yapistiralim
    yeni.paste(res, (0,0))
    yeni.paste(res_filtre_ayna, (0, y)) 

    # sonucu yeniden ebatlandiralim
    yeni = yeni.resize((x//4, y//2))
    
    # nihai sonucu kaydedelim
    yeni.save(f"{islem_yeri}/{os.path.basename(resim)}")

    # display a message
    print(f"{resim} islenme tamam...")
    
    # islemdeki resim dosyalarini kapatalim
    res.close()
    res_filtre.close()
    res_filtre_ayna.close()
    yeni.close()

# ana program bolumu
if __name__ == '__main__':
    
    bas = perf_counter()

    # prosesler olusturuluyor
    pler = [mp.Process(target=resim_isle, args=[resim,]) 
                for resim in resimler]

    # prosesler baslatiliyor
    for p in pler:
        p.start()

    # proseslerin tamamlanmasi bekleniyor
    for p in pler:
        p.join()
    
    bit = perf_counter()
    
    print(f" Toplam islem suresi {bit - bas : 2.5f} saniye oldu")
    
