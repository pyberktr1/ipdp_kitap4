# Bu ornek kilit kullanmak suretiyle bir dizi ip
# arasinda ortak bir mesaj tamponunu paylastirirak
# durum bildiriminin nasıl yapilacagini gostermektedir
# mesaj dokumunu yapan gunce fonksiyonu tazelemeyi
# bir olay nesnesi araciligi ile gercekleştirir

# ip kutuphanesi (kilit nesnesi ile birlikte)
from threading import Thread, Lock, Event
# zamanlayici kutuphanesi
from time import perf_counter, sleep

# ortak hafiza alani
mesaj = []
sayac = 0

# islem ipi
def islem(ipid):
    # mesaj degiskeni global tanimlaniyor
    global mesaj
    
    # lokal degisken tanimlaniyor
    durum = 0
    
    # islem 100 kere tekrarlaniyor
    for i in range(100):
        # asil islev ortak kaynakla dogrudan ilgili
        # olmadigi icin kritik bolge disina aliniyor
        durum = durum + ipid
        sleep(0.1)
        
        # kritik bolgeye giriste destur cekiyoruz
        # musaitse kilit ilgili ipe tayin edilir
        # degilse ilgili ip beklemeye alinir
        # burada with deyimini kullanarak
        # cikista kilitin otomatik serbest 
        # birakilmasini sagliyoruz
        
        with kilit:
            # kritik (hassas) bolge
            # bu kisim sadece kilit iznine sahip olan
            # ipte isletilir
        
            # durum mesaji uretiliyor ve mesaja atiliyor
            mesaj.append(f"{ipid} gorevinde durum ilerlemesi {durum} asamasinda")
  
            # mesaj tamponunda artik bir mesaj var
            # mes_buf_dolu bayragini kaldiriyoruz
            mes_buf_dolu.set()
            
            # ortak kaynak ile isimiz bitti
            # hassas bolgeden cikis gerceklestiriliyor
            # kilit diger iplerin kullanmasi icin serbest birakiliyor
            # with blogunda islem yaptigimiz icin release() e gerek yok

# gunluk ipi
def gunce():
    # mesaj global tanimlaniyor
    global mesaj
    # sayac global tanimlaniyor
    global sayac
    
    # sonsuz dongude mesajlar ekrana dokuluyor
    while True:
        # guncelleme icin bir mes_buf_dolu olayi bekleniyor
        mes_buf_dolu.wait()
        
        # mesaj icin kilit talep ediliyor
        with kilit:
            # birikmis tum mesajlar ekrana yazdiriliyor
            # mesaj kutusu bosaltilincaya kadar yeni
            # mesajlar atilmis olabilir
            # bu sebeple tum mesajlarin bosaltildigindan
            # emin olmamiz gerekiyor
            for i in range(len(mesaj)):
                sayac = sayac + 1
                print(mesaj[i])
        
            # mesaj kutusu bosaltiliyor
            print("*")
            mesaj = []
            
            # mesaj kutusu bosaltildigi icin
            # mes_buf_dolu bayragi indiriliyor
            mes_buf_dolu.clear()

# ana program bolumu
# kilit nesnesi olusturuluyor
kilit = Lock()

# mesaj tamponu dolu bayragi olay nesnesi biciminde tanimlaniyor
mes_buf_dolu = Event()

# baslangic kaydediliyor
bas = perf_counter()

# ipler olusturuluyor ve baslatiliyor
ipler = []
for i in range(1,11):
    ip = Thread(target=islem, args=(i,))
    ip.start()
    ipler.append(ip)

# gunluk ipi olusturuluyor ve baslatiliyor
# sonsuz dongude calistigi icin bu ipimiz
# ana programin bitmesiyle birlikte sonlanacak
# hayalet tipte olmasi sarttir
ip = Thread(target=gunce, daemon=True)
ip.start()

# iplerin tamamlanmasi bekleniyor
# gunluk ipi olan hayalet tipteki "gunce" ipinin
# sonlanmasini beklemek dogru olmaz
# o yuzden gunce icin bekleme yapmiyoruz
for ip in ipler:
    ip.join()
    
# bitis kaydediliyor
bit = perf_counter()

# gunce hayalet ipinin kuyruktaki son mesajlari da ekrana 
# dokmesi icin biraz bekliyoruz ( garanti icin)
mes_buf_dolu.set()
sleep(1)

# nihai sonuclar ekrana getiriliyor
print()
print(f"Tum islemler {bit - bas : 2.5f} saniyede tamamlandi")
print(f"Toplamda {sayac} adet mesaj ekrana yazdirildi")
