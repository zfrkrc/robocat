# RoboCat / sistem

![Kontrol mimarisi](images/robocat-architecture.svg)

## Yerel kontrol
Arduino Mega 2560 R3 yerel hareket kontrolcüsüdür. Mevcut PCA9685 16 PWM kanalı sağlar: 12 bacak servosu ve kol için ayrılan dört kanal. PWM frekansı ortak olduğundan servolarla birlikte doğrulanır. Kullanıcıdaki 16 motor MG996R 180° olarak sipariş edilmiştir; servo merkezleri/yönleri/hareket limitleri fiziksel kalibre edilir.

Gövde MPU6050 verisi kontrol girdisidir; takılması hazır çalışan aktif denge anlamına gelmez. Beş HC-SR04 için ayrı bağlantı ayrılabilir ve ölçümler sırayla tetiklenir. Ön sabit omuzlar için iki, arka için bir sensör hedeflenir; kalan ikisi opsiyoneldir. Son yerleşim bacak hareket hacmiyle doğrulanacaktır.

## Görüş ve merkez
İki ESP32-CAM sabit kafadadır; üçüncüsü gelecekte kol üzerindedir. Görüntü Wi-Fi ile merkeze gider. Merkez hedef/görev üretir; servo döngüsü internet üzerinden tek tek sürülmez. ESP32-C3 köprüsü model/pin doğrulamasına bağlıdır. HC-06 Bluetooth Classic manuel komut için kullanılabilir.

Kişi tanıma, yaklaşık 1 m takip ve kartvizit sunma hedef özelliklerdir; henüz çalıştığı doğrulanmış değildir. İki bağımsız ESP32-CAM senkron stereo derinlik sistemi kabul edilmez. Hedef kaybı/komut bayatlaması davranışı önce gövde destek üzerindeyken test edilir.

## Güç
![Tek LiPo](images/robocat-power.svg)

Tek Tinylab 3S LiPo hedefi, 11,1 V nominal / 12,6 V tam dolu. Hot-swap iptal. 6 V servo ve ayrı 5 V elektronik regülasyonu gerekiyor; kesin regülatör ve sigorta modelleri henüz seçilmedi. XT60 bulunması tüm yolun belli bir akıma uygun olduğunu kanıtlamaz. Servo gücü breadboard/Dupont üzerinden taşınmaz.

## Arayüz ve dokümanlar
- [Pin önerisi](../hardware/PINMAP_REV_A.csv): Nova kaynak koduyla birebir eşleştiği varsayılmaz.
- [Güncel güç/test planı](../hardware/PCB_PLAN_REV_A.md): başlık rev B; dosya adı mevcut bağlantıları korumak için kaldı.
- [Envanter](../hardware/INVENTORY.md).

Şematik, PCB yerleşimi veya RoboCat için doğrulanmış Gerber henüz yoktur. Upstream Gerber'leri orijinal konfigürasyona aittir.
