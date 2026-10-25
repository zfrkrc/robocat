# RoboCat PCB / masaüstü test planı — rev B

2026-10-25. Kullanıcı kararı: HOT-SWAP İPTAL. Tek Tinylab 3S LiPo 11.1 V 2200 mAh 40C, tam dolu 12.6 V. İkinci paket varsa kapalı robotta değiştirilen yedektir; paralel veya seri bağlanmaz. Eski rev A güç mimarisi bu belgeyle değiştirilmiştir.

DURUM: modüllerle masaüstü test öncesi bağlantı planı. Henüz şematik/PCB, ERC/DRC veya siparişe hazır Gerber değildir. Kaynak Nova-SM3 Teensy tabanlı Gerber arşivi mevcut olsa da Mega/MG996R RoboCat için onaylanmış kart değildir.

## Sistem
- Mega 2560 R3 + mevcut PCA9685.
- Toplam 16 MG996R: kanallar 0–11 bacaklar, 12–15 kol için aday. PINMAP_REV_A.csv sinyal önerisidir; orijinal Nova kanal sırasına otomatik uyumlu değildir.
- Bir gövde MPU6050, ikinci opsiyonel; beş HC-SR04 için ayrı sırayla tetikleme.
- Kafada iki ve kolda bir ESP32-CAM; görüntü Wi-Fi ile merkeze, Mega üzerinden değil.
- LCD, HC-06 ve ek sensörler INVENTORY.md içinde.

## Tek paket güç yolu
LiPo XT60 → uygun DC sigorta → yük akımına uygun ana kesme → servo/elektronik kollarına ayrım.
- Servo kolu: uygun 6 V yüksek akım regülatörü → güç dağıtımı → servo beslemeleri.
- Elektronik kolu: ayrı uygun 5 V regülatör → kontrollü Mega beslemesi, kamera ve sensör dalları.
- USB/haricî besleme geri akımı önlenecek; Mega VIN/5 V/USB rastgele birleştirilmeyecek.
- Ortak GND, uygun kablo/konnektör ve yüksek akım dönüş yolu gerekiyor. Breadboard ve sinyal jumperları servo güç hattı değildir.
- LiPo balanslı haricî şarj; balans kablosu BMS anlamına gelmez. Düşük hücre gerilimi izleme/koruma çözümü hâlâ gerekli.
- 6S BMS bu 3S pakete uygun değildir. Sadece hot-swap iptal oldu; sigorta/regülasyon/düşük gerilim koruması iptal olmadı.

## Önce test
1. Haricî doğrulanmış regüle beslemeyle tek servo/PCA/Mega. Servo merkez ve güvenli aralıklar.
2. Tek bacak, sonra destek üstünde 12 bacak; akım, besleme düşümü, ısınma.
3. Kol için ayrılan dört servo; ardından eşzamanlı güç ihtiyacı.
4. Kamera/sensörler ve hareket sırasında reset/gürültü testi.
5. Ölçülmüş akıma göre regülatör, sigorta, konnektör, PCB bakırı/ısı ve mekanik yerleşim seçimi.
6. Şematik, footprint kontrolü, PCB, ERC/DRC, ardından küçük adet prototip siparişi.

## Hâlâ açık
6 V ve 5 V regülatör gerçek modelleri; sigorta/anahtar DC akım değerleri; düşük hücre gerilimi koruması; soket/header dizilimi; PCB gövde montajı; tam yük/ısıl testler. Donanım satın alma listesi bunların hepsinin tamamlandığı anlamına gelmez.

## 3D baskı
Güncel kontrollü liste: ../custom/print-fit-v0.4/print_manifest.json . Bu liste fiziksel yazıcıya entegre edilmedikçe kuyruk üzerinde yaptırım uygulamaz. Orijinal tüm-klasör STL keşfiyle otomatik baskı kullanılmamalı. CAT10 ve eski 18650 parçaları basılmayacak. Yeni LiPo tepsisi yalnız boş uyum prototipidir.
