"""Generate repo-native, exact architecture diagrams. Not electrical schematics."""
from pathlib import Path
from html import escape
P=Path(__file__).resolve().parents[1]/'images';P.mkdir(exist_ok=True)
def start(w,h,title,subtitle):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">', '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0 L0 6 L8 3Z" fill="#5bb8c8"/></marker></defs>',f'<rect width="{w}" height="{h}" rx="24" fill="#0c1723"/>',f'<text x="48" y="55" fill="#edf5fa" font-size="30" font-weight="700" font-family="DejaVu Sans,sans-serif">{escape(title)}</text>',f'<text x="48" y="89" fill="#9db4c5" font-size="17" font-family="DejaVu Sans,sans-serif">{escape(subtitle)}</text>']
def card(a,x,y,w,h,title,lines,kind='normal'):
 stroke='#d3a447' if kind=='pending' else '#345467';fill='#2b251b' if kind=='pending' else '#142736'
 a.extend([f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',f'<text x="{x+20}" y="{y+34}" fill="#f2f6fa" font-family="DejaVu Sans,sans-serif" font-size="21" font-weight="700">{escape(title)}</text>'])
 for i,line in enumerate(lines):a.append(f'<text x="{x+20}" y="{y+65+i*25}" fill="#bdd0dd" font-family="DejaVu Sans,sans-serif" font-size="16">{escape(line)}</text>')
def arrow(a,path,label=None,x=0,y=0):
 a.append(f'<path d="{path}" fill="none" stroke="#5bb8c8" stroke-width="3" marker-end="url(#arrow)"/>')
 if label:a.append(f'<text x="{x}" y="{y}" fill="#83d7e1" font-family="DejaVu Sans,sans-serif" font-size="15">{escape(label)}</text>')
def footer(a,y,lines):
 for i,line in enumerate(lines):a.append(f'<text x="48" y="{y+i*25}" fill="#d7ba7e" font-size="16" font-family="DejaVu Sans,sans-serif">{escape(line)}</text>')
def save(a,n):a.append('</svg>');(P/n).write_text('\n'.join(a))
a=start(1400,920,'RoboCat / kontrol ve görüş mimarisi','Planlanan bağlantılar • modüller mevcut • kablolama ve yazılım testleri bekliyor')
card(a,500,125,400,120,'MERKEZ SUNUCU',['Kişi / nesne tanıma, görev planı','Hedef takip ve kartvizit görevi'])
card(a,55,320,360,130,'3 × ESP32-CAM',['2 sabit göz + 1 kol kamerası','Görüntü Wi-Fi ile merkeze gider'])
card(a,520,320,360,130,'ESP32-C3 köprüsü',['UART ile Mega bağlantısı adayı','Fiziksel ESP pinleri doğrulanacak'],'pending')
card(a,985,320,360,130,'HC-06 / manuel komut',['Bluetooth Classic','Mega Serial1; lojik seviye uyumu'])
card(a,55,550,360,145,'SENSÖRLER',['MPU6050, HC-SR04, LCD','Diğer sensörler aşamalı eklenecek','Besleme / I²C seviyeleri kontrolü'])
card(a,520,550,360,145,'ARDUINO MEGA 2560',['Yerel hareket döngüsü','Servo kalibrasyonu, sensör okuma','Bağlantı kaybında davranış'])
card(a,985,550,360,145,'PCA9685 / 16 PWM',['CH 0–11: bacaklar','CH 12–15: kol için ayrılmış','Servo gücü ayrı dağıtılır'])
card(a,985,770,360,95,'16 × MG996R',['12 bacak + 4 kol adayı'])
arrow(a,'M235 320 L500 205','Wi-Fi görüntü',255,270)
arrow(a,'M700 245 L700 320','Wi-Fi komut',715,285)
arrow(a,'M700 450 L700 550','UART + seviye uyumu',715,505)
arrow(a,'M1120 450 L880 590','UART',1040,493)
arrow(a,'M415 620 L520 620','I²C / GPIO',421,603)
arrow(a,'M880 620 L985 620','I²C + OE',891,603)
arrow(a,'M1165 695 L1165 770','PWM sinyali',1180,737)
footer(a,785,['Bu diyagram devre şeması / PCB değildir.','Kamera verisi Mega üzerinden taşınmaz.','Kol ve takip henüz tamamlanmış özellikler değildir.'])
save(a,'robocat-architecture.svg')
a=start(1450,840,'RoboCat / tek LiPo güç düzeni','Hot-swap iptal • pil değişiminde robot kapatılır • voltaj hatları henüz fiziksel test edilmedi')
card(a,50,190,285,145,'TEK 3S LiPo',['Tinylab 2200 mAh / 40C','11,1 V nominal / 12,6 V dolu','XT60 • balanslı haricî şarj'])
card(a,405,190,285,145,'KORUMA + KESME',['Uygun DC sigorta ve anahtar','Düşük hücre gerilimi koruması','Parça ve eşikler seçilecek'],'pending')
card(a,950,140,360,145,'6 V SERVO REGÜLATÖRÜ',['Yüksek akım / geçici yük hesabı','Model ve akım kapasitesi açık','Servo beslemesine doğrudan pil yok'],'pending')
card(a,950,365,360,145,'5 V ELEKTRONİK HATTI',['Mega, kameralar ve sensörler','USB geri beslemesi önlenecek','Gaz ısıtıcıları bütçeye eklenecek'],'pending')
card(a,950,585,360,110,'YÜKLER / DAĞITIM',['Servolar ve elektronik ayrı dallar','Ortak GND, doğru dönüş yolları'])
arrow(a,'M335 260 L405 260','DC',355,245)
arrow(a,'M690 260 L805 260 L805 212 L950 212','Servo kolu',816,195)
arrow(a,'M805 260 L805 435 L950 435','Elektronik kolu',807,416)
arrow(a,'M1310 212 L1370 212 L1370 620 L1310 620')
arrow(a,'M1130 510 L1130 585')
footer(a,735,['BMS, regülatör ve şarj cihazı aynı işlev değildir. 6S BMS bu 3S pakete uygun değildir.','Bu bir güç mimarisi diyagramıdır: sigorta / kablo / regülatör değerleri seçilip test edilmeden üretime gönderilmez.','Yedek paket varsa kapalı robotta değiştirilir. İki paket doğrudan paralel bağlanmaz.'])
save(a,'robocat-power.svg')
print('Generated 2 SVG diagrams.')
