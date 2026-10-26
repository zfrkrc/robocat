# RoboCat — gerçek proje ve donanım fotoğrafları

Tarih: 2026-10-26. Kullanıcının paylaştığı 20 fotoğraf. Görseller yönü düzeltilmiş ve EXIF/konum verileri aktarılmadan web için küçültülmüştür. Orijinal dosya adı her başlıkta korunur.

Fotoğraf bir örneğin fiziksel görünümünü belgeler; siparişin tamamının teslimini, adet sayımını, elektriksel testi veya montaj uyumunu doğrulamaz. Yeni siparişlerin teslim durumları bu karelerden topluca değiştirilmedi. Tanımlanamayan kartlar kesin model gibi kaydedilmedi.

[Ana kurulum ve kabul takibi](KURULUM.md) · [Envanter](../hardware/INVENTORY.md) · [Galeri](GALLERY.md)

## IMG_9220 — Yazıcı içinde kafa parçalarının baskı aşaması

![Yazıcı içinde kafa parçalarının baskı aşaması](images/build-2026-10-26/img_9220.jpg)

## IMG_9221 — Yazıcı ve baskı tablasının genel görünümü

![Yazıcı ve baskı tablasının genel görünümü](images/build-2026-10-26/img_9221.jpg)

## IMG_9230 — HW-373 V1.2 1S Li-ion şarj / 5 V boost modülü — geliştirme kartı değil

![HW-373 V1.2 1S Li-ion şarj / 5 V boost modülü](images/build-2026-10-26/img_9230.jpg)

Kart üzerindeki serigrafi **`HW-373 V1.2`** olarak okunuyor. Micro-USB girişli, **B+ / B-** pil ve **OUT+ / OUT-** çıkış pad'leri var; 8 bacaklı iki anahtarlama/protection çipi ile orta boy bir boost çipi görülüyor. Bu bir **tek hücre (1S, 3,7 V) Li-ion şarj + 5 V yükseltici (powerbank tipi) modüldür**, Arduino/geliştirme kartı değildir: ATmega, USB-seri çip, erkek header veya lojik pin yok.

- **RoboCat güç planıyla uyumsuz:** proje 3S 11,1 V 2200 mAh LiPo + 6 V servo / 5 V elektronik hattı kullanıyor. Bu kart 1S girişlidir; 3S pakete bağlanmaz.
- Tek başına 5 V deneme beslemesi olarak kullanılabilir; servo akımı, sigorta ve düşük gerilim koruması sağlamaz.
- Kesin çıkış akımı ve çip modelleri fotoğraftan doğrulanamaz; yükle test edilmeden RoboCat güç yolu sayılmaz.

## IMG_9234 — ESP32-CAM ve kamera modülü

![ESP32-CAM ve kamera modülü](images/build-2026-10-26/img_9234.jpg)

## IMG_9235 — GY-521 / MPU6050 kartı

![GY-521 / MPU6050 kartı](images/build-2026-10-26/img_9235.jpg)

## IMG_9236 — Bluetooth seri modülünün arka yüzü

![Bluetooth seri modülünün arka yüzü](images/build-2026-10-26/img_9236.jpg)

## IMG_9237 — Bluetooth seri modülünün ön yüzü — HC-06 siparişiyle eşleştirme adayı

![Bluetooth seri modülünün ön yüzü — HC-06 siparişiyle eşleştirme adayı](images/build-2026-10-26/img_9237.jpg)

## IMG_9238 — T413 LDS/taret kartı — robot süpürgeden sökülmüş, RoboCat envanteri değil

![T413 LDS/taret kartı](images/build-2026-10-26/img_9238.jpg)

Serigrafide **`T413`** yazıyor. Altı adet optik alıcı/verici ve ortada döner mekanizma boşluğu var; bu, bir robot süpürgenin **lazer mesafe/liDAR (LDS) taret kartıdır**. RoboCat'in kafa kamerası veya HC-SR04 ultrasonik hattıyla ilgisi yoktur; pinout ve sürücü entegresi bilinmiyor. Envantere alınmaz, yedek/deney parçası sayılır.

## IMG_9240 — 16×2 LCD ve I²C adaptörü

![16×2 LCD ve I²C adaptörü](images/build-2026-10-26/img_9240.jpg)

## IMG_9243 — SD kart modülü — ek deney donanımı

![SD kart modülü — ek deney donanımı](images/build-2026-10-26/img_9243.jpg)

## IMG_9245 — İki hoparlör — güç/empedans ve kullanım teyit bekliyor

![İki hoparlör — güç/empedans ve kullanım teyit bekliyor](images/build-2026-10-26/img_9245.jpg)

## IMG_9246 — Aç/kapa anahtarı — DC akım etiketi doğrulanacak

![Aç/kapa anahtarı — DC akım etiketi doğrulanacak](images/build-2026-10-26/img_9246.jpg)

## IMG_9248 — Dreame fırçasız (BLDC) motor — süpürge parçası, servo değil

![Dreame fırçasız motor](images/build-2026-10-26/img_9248.jpg)

Gövdede **`上海追觅科技` (Shanghai Dreame Technology)** ve **`019-200330 ZD`** ile `RoHS` yazıları var. Arka tarafta 5 kablolu küçük devre kartı bulunuyor. Bu bir **fırçasız DC (BLDC) motor** adayıdır; servo değildir, PCA9685'in 50 Hz servo sinyaliyle veya tek yönlü DC sürücüyle çalışmaz. Sürmek için uygun **3 fazlı ESC/BLDC sürücü**, Hall/encoder okuma ve kapalı çevrim gerekir. Faz/Hall pinout'u ölçülmeden bağlanmamalıdır.

## IMG_9249 — MG996R servo ve çıkış mili

![MG996R servo ve çıkış mili](images/build-2026-10-26/img_9249.jpg)

## IMG_9251 — PRI-3605U-15260 fırçasız motor + arka kart — süpürge parçası

![PRI-3605U-15260 motor](images/build-2026-10-26/img_9251.jpg)

Gövdede **`PRI-3605U-15260`** ve **`20.02`** damgası okunuyor; arkasında 5 kablolu yeşil encoder/sürücü kartı ve çıkışta küçük bir dişli var. Bu da **Dreame süpürge kaynaklı, büyük olasılıkla fırçasız (BLDC)** bir motordur.

- **MG996R yerine kullanılmaz:** bacak eklemleri pozisyon kontrollü servo istiyor; bu motorun açısal referansı ve redüktör çıkışı servo gibi sabitlenmez.
- **Tahrik/deney için şartlı kullanılabilir:** sadece uygun BLDC sürücü + Hall okuma + kapalı çevrim kontrol ile. 5 kablonun hangisi faz, hangisi Hall/besleme olduğu **ölçülerek** bulunmalı; yanlış bağlama sürücüyü yakar.
- Servo sinyali (PCA9685), L298N/BTS7960 tipi basit DC sürücü veya doğrudan 3S bağlantı **uygun değildir**.

## IMG_9252 — Dreame MOTOR_CONN_B0_v2 motor bağlantı kartı — süpürge parçası

![Dreame motor bağlantı kartı](images/build-2026-10-26/img_9252.jpg)

Serigrafi **`MOTOR_CONN_B0_v2`** ve **`Dreame`** markasını gösteriyor. Sökülmüş bir robot süpürgenin motor/fırça bağlantı kartıdır; üzerindeki altın kaplama flex kontaklar aşınmış görünüyor. RoboCat BOM'una girmez, sürücü veya güç dağıtım kartı olarak kullanılamaz.

## IMG_9253 — Aynı motor bağlantı kartının soket yüzü

![Motor bağlantı kartı soket yüzü](images/build-2026-10-26/img_9253.jpg)

## IMG_9254 — Sökülmüş süpürge redüktörü, kart yüzü

![Sökülmüş süpürge redüktörü, kart yüzü](images/build-2026-10-26/img_9254.jpg)

## IMG_9255 — Redüktör dişli grubunun iç görünümü

![Redüktör dişli grubunun iç görünümü](images/build-2026-10-26/img_9255.jpg)

## IMG_9256 — Motor ve redüktör çıkış detayı

![Motor ve redüktör çıkış detayı](images/build-2026-10-26/img_9256.jpg)


## Sınıflandırma

| Grup | Fotoğraflar | RoboCat'te yeri |
|---|---|---|
| 3B baskı | IMG_9220, IMG_9221 | Baskı aşaması kaydı; kabul testi değil |
| RoboCat'e uygun elektronik | IMG_9234 (ESP32-CAM), IMG_9235 (MPU6050), IMG_9236/9237 (Bluetooth), IMG_9240 (LCD), IMG_9243 (SD), IMG_9245 (hoparlör), IMG_9246 (anahtar), IMG_9249 (MG996R) | Envanter/deney adayı; her biri ölçümle doğrulanacak |
| Güç modülü — uyumsuz | IMG_9230 (HW-373, 1S şarj + boost) | 3S planında kullanılmaz; yalnız 1S masaüstü denemesi |
| Robot süpürgeden sökülmüş parçalar | IMG_9238 (T413 LDS), IMG_9248 ve IMG_9251 (BLDC motor), IMG_9252/9253 (MOTOR_CONN kartı), IMG_9254–9256 (redüktör) | RoboCat BOM'unda yok; kaynak/yedek parça |

Bu tablo fotoğrafın ne gösterdiğini sınıflandırır; adet, teslim ve elektriksel test teyidi değildir. Model etiketi okunamayan kartlar kesin model olarak kaydedilmedi.

## Arduino ve USB-seri durumu — 2026-10-26

Aynı gün yapılan bağlantı teşhisi (fotoğraflardan bağımsız):

- Bilgisayarda `/dev/ttyUSB0` üzerinde **CH340** (`1a86:7523`) USB-seri dönüştürücü görünüyor; `ttyACM*` yok.
- 1200–250000 baud arası okumada **0 bayt**; DTR reset sonrası bootloader çıktısı yok.
- `avrdude -c arduino` ile **mega2560, atmega328p** imza okuma denemeleri **12/12 `not in sync: resp=0x00`**. Manuel reset de sonucu değiştirmedi.
- Sonuç: **Arduino Mega R3 henüz doğrulanmadı.** Ya kart bağlı değil, ya TX/GND hattı/PWR sorunlu. Fotoğraflarda da Arduino kartı yok (IMG_9230 bir güç modülüdür). Mega fiziksel olarak doğrulanana kadar yürüyüş firmware'i yüklenmiş sayılmaz.

## İlgili

- [Kurulum ve sipariş kabul takibi](KURULUM.md)
- [Envanter](../hardware/INVENTORY.md)
- [Galeri](GALLERY.md)
- [Kaynak notları](SOURCES.md)
