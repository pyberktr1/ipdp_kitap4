# Bu ornek bir resim isleme prosesini gosterir

# zamanlayici kutuphanesi
from time import perf_counter
# isletim sistemi fonksiyonlari
import os
# resim isleme kutuphanesi
from PIL import Image as Resim, ImageFilter as ResFiltre, \
    ImageOps as Resislem

# resim dosyalari
resimler = [
    "./resim/1.jpg",
    "./resim/2.jpg",
    "./resim/3.jpg",
    "./resim/4.jpg",
    "./resim/5.jpg",
]

# resim isleme fonksiyonu
def resim_isle(resim, islem_yeri ='./'):
    # resim dosyasini acalim
    res = Resim.open(resim)

    # resim uzerinde bir islem yapalim
    yeni = Resislem.invert(res)
    yeni.show("NEGATİF")

    yeni = Resislem.posterize(res, 2)
    yeni.show("POSTER")

    yeni = Resislem.solarize(res, 80)
    yeni.show("SOLDURMA")

    yeni = Resislem.grayscale(res)
    yeni.show("GRİ SKALA")

    # Gauss bulanıklaştırma filtresi
    yeni = res.filter(ResFiltre.GaussianBlur(16))
    yeni.show("BULANIK")
    
    # Filtrelenmis resmi dikey eksende aynalayalim
    yeni = res.transpose(method=Resim.FLIP_TOP_BOTTOM)
    yeni.show("AYNA TERSI")

    # nihai sonucu kaydedelim
    yeni.save(f"{islem_yeri}/{os.path.basename(resim)}")
    
    # display a message
    print(f"{resim} islenme tamam...")
    
    # islemdeki resim dosyalarini kapatalim
    res.close()
    yeni.close()

# ana program bolumu
if __name__ == '__main__':
    
    resim_isle(resimler[0])    
