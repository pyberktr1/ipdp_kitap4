# yuzde kodlanmis html stringleri, 
# utf-8 kodlanmis stringlere donusturen arac
# yuzde kodlanmis html string
d_ad = "Devrim_at_T%c3%bclomsa%c5%9f.jpg"
# once bytearray halinde ikili kodlara donusturuyoruz
dm=bytearray()
i=0
while i < len(d_ad):
    if d_ad[i]=="%":# yuzde kod, utf-8 byte koda donusuyor
        hexstr="0x"+d_ad[i+1]+d_ad[i+2]
        dm.append(int(hexstr, 0))
        i=i+2# dongu iki ilerletiliyor, donusturulen karakterler atlaniyor
    else:# normal karakterler aynen kopyalaniyor
        dm.append(ord(d_ad[i]))
    # dongu normal bicimde ilerletiliyor
    i=i+1

print("byte array   :",dm)
dmstr=dm.decode()
print("utf-8 string : ",dmstr)

