# RoboCat PCB bağlantı planı — rev A taslak

2026-10-25. DURUM: bağlantı planı; henüz şematik, PCB yerleşimi, ERC/DRC raporu veya üretilebilir Gerber değildir. Bu belgeyi PCB üretimine göndermeyin.

## Kesinleşen mimari
- Arduino Mega 2560 R3 CH340 klon; mevcut modül kabloyla bağlanacak. Mega Pro footprinti kullanılmayacak.
- Mevcut PCA9685 modülü: 16 PWM kanalı. 0–11 bacaklar, 12–15 kol için ayrılır. Kol motorlarının mekanik/tork uygunluğu ayrı doğrulanacak.
- 3 ESP32-CAM kendi Wi-Fi bağlantılarıyla merkeze görüntü gönderir. Mega kamera veri yolu taşımaz.
- Mevcut ESP32-C3, model/pinleri doğrulandıktan sonra merkez köprüsü olabilir; şimdilik sadece UART sinyalleri ayrılır.
- 2 adet aynı model Tinylab 11.1 V 3S 2200 mAh 40C LiPo hedefi; satın alma/adet henüz kullanıcı tarafından açıkça teyit edilmedi. İki paket 3S olarak bağımsız kalır; 6S yapılmaz.
- Satıcı verisi: paket 108×35×21 mm, 167.1 g, XT60, kablo 75 mm. Bu ölçüler kablo/konnektör hareket payı ve yumuşak LiPo muhafaza toleransı yerine geçmez. Kaynak: https://www.robotistan.com/tinylab-111v-3s-lipo-batarya-2200mah-40c
- Eski 18650 kutuları bu LiPo için kullanılmayacak.

## Kart sınırları
KONTROL TAŞIYICISI: modül bağlantıları, lojik seviye eşleştirmeleri, giriş koruma/filtreleme ve test noktaları. İlk sürümde mevcut modülleri tekrar satın aldıran gömülü sensör tasarımı yapılmayacak.
GÜÇ BÖLÜMÜ: paket başına sigorta/koruma; ters akım engelleme ve takma akımı sınırlamalı güç yolu; 6 V servo ve ayrı 5 V elektronik regülasyonu. Regülatör ve hot-swap parçaları seçilmediği için bu bölüm üretime hazır değildir. BMS, regülatör ve hot-swap aynı işlev değildir. RC LiPo'nun balans kablosu BMS bulunduğu anlamına gelmez; her hücreyi izleyen düşük gerilim koruması gereksinimi tasarımda açık tutulur. Haricî 3S LiPo balanslı şarj kullanılır.

## Servo sinyal sırası
| PCA9685 kanal | Görev |
|---:|---|
| 0,1,2 | Ön sağ: yana açılma, üst bacak, diz |
| 3,4,5 | Ön sol: yana açılma, üst bacak, diz |
| 6,7,8 | Arka sağ: yana açılma, üst bacak, diz |
| 9,10,11 | Arka sol: yana açılma, üst bacak, diz |
| 12 | Kol taban dönüşü |
| 13 | Kol omuz |
| 14 | Kol dirsek |
| 15 | Kavrayıcı / yaylı mekanizma sürüşü |

Bu RoboCat için yeni önerilen sıralamadır; Nova yazılımındaki kanalların birebir karşılığı değildir. Orijinal yazılımı bu sıraya uyarlamadan kullanmayın. PCA9685 yalnız PWM üretir; servo akımını kendi entegresinden taşımaz. Tek sürücü tüm kanallarda ortak PWM frekansını kullanır; MG996R için gerçek örneklerle frekans/merkez/aralık kalibrasyonu gerekir.

## Arayüz kuralları
- Mega I²C: D20 SDA, D21 SCL. PCA9685/LCD ve 3.3 V sensörler için uygun gerilim bölgeleri; I²C pull-up'ları fiziksel modüller üzerinde incelenecek.
- PCA9685 VCC lojik besleme; V+ servo besleme, birbirine karıştırılmaz. OE donanımsal pull-up ile başlangıçta devre dışı; D8 kontrollü etkinleştirme.
- D9 servo güç talebi olarak ayrıldı; doğrudan yüksek akım yük sürmez. Donanımsal kesme elemanı henüz seçilmedi. OE tek başına fiziksel güç kesmesi değildir.
- Mega 5 V TX çıkışları HC-06/ESP 3.3 V RX'e doğrudan bağlanmayacak. APDS/MPU modüllerinin besleme ve pull-up düzeni incelenecek.
- MQ, mikrofon, alev ve ACS712 modüllerinin pin sırası/çıkış aralığı doğrulanacak; pin başlıkları tek bir tahmini A0/D0 dizilimine göre üretilmeyecek.
- QRE1113GR çıplak eleman olabilir; LED direnci ve fototransistör okuma devresi gerekir. Load cell için uygun yükselteç/ADC (HX711 adayı) listede yok.
- Beş ultrasonik sensör aynı anda tetiklenmez.
- Ana servo beslemesi ve kamera beslemeleri haricî güç dağıtımından gelir. Breadboard/Dupont üzerinden servo akımı geçirilmez. Ortak toprak dönüşü servo gürültüsünü sensör referansına taşımayacak şekilde tasarlanır.
- Gaz sensörleri ısıtıcıları için ayrı güç bütçesi/ısıl yerleşim gerekir; mevcut burun parçası ısıtıcı yuvası değildir.
- USB ve haricî 5 V kaynaklarının geri beslemesi önlenecek; Arduino 5 V/VIN/USB rastgele birbirine bağlanmayacak.

## Üretim öncesi açık kalanlar — kullanıcıdan tekrar envanter istenmiyor
1. Servo 6 V regülatörünün gerçek üretici/modeli, tam yük ve transient davranışı; 16 servo için ölçülmüş akım bütçesi.
2. Elektronik 5 V regülatörünün gerçek modeli, kamera ve gaz ısıtıcıları dahil kapasitesi.
3. Paket başına koruma, sigorta, hot-swap denetleyicisi, MOSFET ve akım sınırlaması seçimi; ters akım ve servodan geri gelen enerji değerlendirmesi.
4. Gerçek modüllerin header/soket ve PCB montaj ölçüleri; mevcut liste bu ölçüleri sağlamaz. Modüller için kablolu arayüz kullanılarak yanlış footprint riski azaltılacak.
5. PCB dış ölçüsü, sabit gövde montajı, yüksek akım kablo/konnektör ve soğutma hesabı.
6. Şematik/PCB oluşturma, ERC/DRC, netlist-pin kontrolü, 3D çakışma ve düşük enerjili ilk çalıştırma testleri.

Bu dosya tamamlanmış PCB yerine sunulmaz. Yazıcı otomasyonuna ait bir dosya değildir; STL/G-code değiştirmez.
