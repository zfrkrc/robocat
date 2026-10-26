# RoboCat — kurulum

Kurulumu üç aşamaya ayırıyorum: **yazılım**, **elektronik**, **mekanik**. Aşağıdaki maddelerin bir kısmı **kod değişikliği** veya **satın alma** gerektirir; tamamlanmış kurulum yoktur.


## Sipariş ve kabul takibi — 2026-10-26

Ana izleme yeri bu kurulum klasörüdür. **Sipariş verildi ≠ teslim alındı ≠ test edildi.** Aşağıdaki siparişler **2026-10-26'da teslim alındı** (kullanıcı bildirimi); adet sayımı, fotoğraf kaydı ve elektriksel testler henüz yapılmadı.

| Parça | Sipariş | Teslim alınan | Test edilen | Kullanım / sonraki adım |
|---|---:|---|---|---|
| TCA9548A I²C çoklayıcı | 2 | ✅ 2026-10-26 | 0 | 1 kullanım + 1 yedek; kanal/adres eşlemesi firmware ile doğrulanacak |
| PWM DC motor hız kontrolü 1,8–12 V / 2 A | 2 | ✅ 2026-10-26 | 0 | Servo regülatörü değildir; dolu 3S (12,6 V) doğrudan bağlanmaz |
| Dijital DC voltmetre, kırmızı | 2 | ✅ 2026-10-26 | 0 | Batarya ve 6 V hattı göstergesi adayı; hücre koruması değildir |
| USB 5 V ultrasonik sis yapıcı | 1 | ✅ 2026-10-26 | 0 | Sonraki efekt aşaması; ilk yürüyüşe dahil değil |
| HC-SR501 PIR | 1 | ✅ 2026-10-26 | 0 | Opsiyonel hareket algılama; pin tahsisi henüz yok |
| XL4016 düşürücü regülatör, Robo90 200W başlıklı | 2 | ✅ 2026-10-26 | 0 | Bir kart 5 V elektronik, bir kart 6 V tek-servo/tek-bacak testine aday |

**XL4016 kabul koşulu:** Satıcı 8 A çıkış, 5 A üzerinde ek soğutma belirtiyor. 6 V × 8 A = 48 W; “200W” başlığı 6 V'ta 200 W veya 15–20 A garantisi değildir. 12–16 servonun yürüyüş beslemesi henüz onaylanmadı. Kartlar arası çıkış paralelleme yok; bataryadan ayrı girişler ve ortak GND. Yük bağlamadan multimetreyle 5,0 / 6,0 V ayarlanır; yük altında gerilim, akım ve sıcaklık kaydedilir. Bu modüllerin ayarlanabilir akım limiti olduğu varsayılmaz; test beslemesinde uygun akım koruması gerekir.

### Kabul kontrol listesi

- [x] Kargo teslimi kullanıcı tarafından bildirildi (2026-10-26)
- [ ] Gerçek adet ve kart fotoğraflarıyla teslim teyidi
- [ ] XL4016 model/pin/polarite kontrolü ve yüksüz çıkış ayarı yapıldı
- [ ] 5 V elektronik hattı yük/ısınma testi geçti
- [ ] 6 V tek servo, ardından üç servolu bacak testi geçti
- [ ] TCA9548A kanal taraması ve firmware kanal eşlemesi doğrulandı
- [ ] Voltmetreler multimetreyle karşılaştırıldı
- [ ] Sonuçlara göre bütün robotun servo kaynağı kararı verildi

Sipariş kaynakları: [Robolink TCA9548A](https://www.robolinkmarket.com/tca9548a-i2c-coklayici), [PWM kart](https://www.robolinkmarket.com/pwm-dc-motor-hiz-kontrol-devresi-18-12v-2a), [voltmetre](https://www.robolinkmarket.com/dijital-dc-voltmetre-kirmizi), [sis yapıcı](https://www.robolinkmarket.com/usb-ultrasonik-nem-buhar-yapici-modul-5v-sis-yapici), [PIR](https://www.robolinkmarket.com/hc-sr501-ayarlanabilir-ir-hareket-algilama-sensoru-pir), [XL4016](https://www.robo90.com/xl4016-dc-dc-step-down-dusurucu-voltaj-regulatoru-200w).

## Fiziksel proje kaydı

[Proje ve donanım fotoğrafları — 20 kare](BUILD_PHOTOS_2026-10-26.md). Baskı durumu ve görülen donanım burada izlenir. Fotoğraflar sipariş adetlerinin tümünün teslimini veya test kabulünü otomatik doğrulamaz; yukarıdaki teslim/test alanları ayrıca güncellenir.

## A) Yazılım kurulumu

1. **Arduino IDE 2.x** kur.
2. Kütüphaneler: depodaki `Nova-SM3/Code/Arduino Libraries/` klasörünü kullan.
   - Klasör halinde olanları `~/Arduino/libraries/` içine kopyala (Adafruit_GFX, Adafruit_NeoPixel, Adafruit-PWM-Servo-Driver-Library, Adafruit_SSD1331, EEPROM, NewPing, PS2X_lib, SPI, T4_PowerButton, Wire).
   - `.zip` olanı (DFRobot_DF1201S) IDE → Sketch → Include Library → Add .ZIP Library ile ekle.
3. Sketch: `Nova-SM3/Code/Nova-SM3_mega-v4.2/Nova-SM3_mega-v4.2.ino` (+ `AsyncServo.h`, `NovaServos.h` aynı klasörde kalmalı).
4. Kart: **Arduino Mega or Mega 2560**, işlemci **ATmega2560**, doğru port. Yüklemeden sonra Seri Monitör 115200.

### USB bağlantı teşhisi — 2026-10-26 (yükleme öncesi bloke)

Mega takılıyken yapılan ölçüm:

- `/dev/ttyUSB0` üzerinde **CH340** (`1a86:7523`) görünüyor; `ttyACM*` yok.
- 1200–250 000 baud arası okumada **0 bayt**; DTR reset sonrası bootloader çıktısı yok.
- `avrdude -c arduino` ile mega2560 ve atmega328p imza okuma: **12/12 `not in sync: resp=0x00`**. Manuel reset sonucu değiştirmedi.

**Sonuç:** Mega'nın bağlı ve çalışır olduğu doğrulanmadı. Yükleme denemesi yapmadan önce sırayla: kartta PWR LED'i, hub'sız USB portu, TX/RX ve GND sürekliliği, 5 V besleme. Fotoğraflardaki `HW-373` modülü Arduino değil, 1S şarj/boost modülüdür.

### Firmware ile donanım farkları (kurulumu bloke eder)

| Konu | Firmware ne bekliyor | Bizde ne var | Gereken |
|---|---|---|---|
| I²C çoklayıcı | **TCA9548A** (`tca_select(tca_pwm)` / `tca_mpu`) | 2 adet teslim alındı (2026-10-26); kanal testi yok | Kanal eşlemesini mevcut firmware ile doğrula; gerekirse kodu düzenle |
| Kumanda | **PS2 alıcı** (`PS2X`) | **HC-06** Bluetooth | HC-06 için Serial1 komut protokolü yazılmalı |
| PWM kanalı | 2 sürücü kimliği (1/2) | 1× PCA9685 | 16 servo = tek kartın **tamamı**; ek kanal yok |

TCA'nın alınması firmware kanal eşlemesini otomatik doğrulamaz. HC-06 komut katmanı ve tek PCA9685 yapılandırması tamamlanmadan firmware olduğu gibi kullanılmaz.

## B) Elektronik kurulum (öneri — fiziksel doğrulama bekliyor)

![Bağlantı şeması](images/robocat-wiring.svg)

*Renkler: güç, I²C, PWM, seri, GPIO. Şema blok seviyesindedir; kablo kesiti ve modül pinleri ayrıca doğrulanır.*

Pin önerisi: [PINMAP_REV_A.csv](../hardware/PINMAP_REV_A.csv). Bu tablo **öneridir**, gerçek modül/pin kontrolü yapılmadı.

```
3S LiPo → XT60 → sigorta → ana kesme
   ├── 6 V regülatör ──► servo barası (PCA9685 V+)
   └── 5 V regülatör ──► Mega / HC-06 / sensörler
```

| Bağlantı | Not |
|---|---|
| PCA9685 SDA/SCL → Mega D20/D21 | I²C; modül 3,3/5 V seviyesi doğrulanacak |
| PCA9685 OE → D8 | Açılışta devre dışı (pull-up) |
| PCA9685 V+ | **6 V servo barası** (LiPo değil), GND ortak |
| HC-06 TX → D19 / RX → D18 | Mega Serial1; seviye dönüşümü kontrol edilecek |
| MPU6050 | I²C (TCA yoksa 0x68) |
| HC-SR04 ×3–5 | D34–D43 (5 V) |
| Servo kanalları | 0–11 bacak, 12–15 kol (koddaki sıra farklı olabilir) |

Kurallar: servo gücü breadboard/Dupont'tan geçmez; ortak GND tek noktada; USB ile harici besleme aynı anda ters besleme yapmayacak.

## C) Mekanik montaj sırası

![Montaj sırası](images/robocat-assembly.svg)

*Sekiz adım, her adımda kuru deneme. Ölçüler kesitle doğrulanmış değerlerdir; baskı toleransı ayrıca denenir.*

1. **Servo merkezleme:** horn takmadan önce her servoyu orta noktaya getir (≈1500 µs / 307 tick @60 Hz).
2. **Horn:** servonun kutusundan çıkan **plastik 25T hornu** servo dişlisine oturt, merkez vidasını sık (vida boyu dibe vurmasın). Horn-parça delik deseni **10,0 mm** (ikincil 13,9 mm) — takmadan önce kuru dene. Yükte kayma/diş sıyırma olursa alüminyum horna geç.
3. **Rulman (625 · 5×16×5):** Ø16 cebe oturt, Ø5 mil geçir. Cep derinliği ölçümü ≈3,6–4,0 mm; rulman 1 mm dışarıda kalırsa cebi 5,2 mm'ye ream et.
4. **Bacak zinciri:** coax → femur → tibia; M3 geçiş, M4 pivot. Sıkma sırasında eklem serbest mi kontrol et.
5. **Kafa:** yüz + kasa + arka kapak; burun ve göz çerçevesi **yapıştırma** (nötr silikon/CA, ince film, IPA temiz yüzey, 24 saat).
6. **Kablolama:** servo uzatmaları eklem içinden geçir, hareket açıklığında sıkışma olmasın.
7. **Son montaj:** kafa gövdeye en son; ağırlık merkezi ve yürüyüş dengesi testte kontrol edilir.

Göz çerçevesi alternatifi: `custom/robocat-v0.3/stl/CAT06B_eye_bezel_7x7_boss_x2.stl` (vidasız, Ø19,6 merkezleme bileziği).

## D) İlk açılış kontrol listesi

- [ ] Servo barası **6,0 V** ölçüldü, GND ortak, sigorta takılı
- [ ] I²C tarama: PCA9685 (0x40), MPU6050 (0x68) görünüyor
- [ ] Tek servo: merkez, yön, güvenli min/maks (bkz. [Kılavuz](KILAVUZ.md) §6)
- [ ] Tek bacak: sıkışma yok, 5 dk tutmada servo gövdesi <60 °C
- [ ] Kalibrasyon: `servoHome` / `servoLimit` MG996R için **yeniden** çıkarıldı
- [ ] Destekli gövde: 3 → 6 → 12 servo kademeli, akım/gerilim kaydı
- [ ] HC-06 bağlantısı ve acil durdurma davranışı test edildi

## E) Kurulumu bloke eden eksikler

**Satın alınacak:** LiPo düşük gerilim alarmı/koruması · DC sigorta + ana kesme · M3/M4 vida-somun.

**Ertelenen / koşullu:** 25T alüminyum horn — ilk denemeler servonun kutusundan çıkan **plastik horn** ile yapılacak; kayma/sıyırma olursa alınacak. HX711 — zorunlu değil. 3S balanslı şarj — elde olduğu hatırlanıyor; LiPo ile gelmezse alınacak.

**Elde, test/kod bekliyor:** 2× 3S LiPo hücre gerilimi/XT60 kontrolü · 6 V servo regülatörünün yüksüz ayarı + kademeli yük testi (12 servo için kapasite onayı yok) · 2× XL4016 yük testi · 2× TCA9548A kanal + firmware eşlemesi · 2× PWM hız kontrolü, 2× voltmetre, sis yapıcı, PIR kabul testi · 625 rulman cep/geçme testi · kablo/konnektör/servo uzatma kesit ve pin kontrolü · Arduino Mega USB teyidi (CH340 var, avrdude sync yok) · **PS2 → HC-06 kod düzenlemesi**.

### Düz anlatım: LiPo alarmı ve sigorta neden gerekli

- **LiPo düşük gerilim alarmı (madde 3):** 3S pakette 3 hücre var. Bir hücre **3,0 V altına** inerse pil kalıcı bozulur, şişer ve yangın riski taşır. Robot yürürken bunu fark etmez, çekmeye devam eder. En basit çözüm, pilin **balans soketine takılan 3S alarm/buzzer**'dır (kablo kesmeye gerek yok); hücre 3,3–3,5 V'a düşünce öter. Alternatif: ACS712 + yazılımda gerilim/akım izleme ve kesme.
- **DC sigorta + ana kesme (madde 4):** 40C/2200 mAh paket kısa devrede **80 A'ya kadar** verebilir; kablo erir, yangın çıkar. Sigorta bu akımı keser. Yuvaya uygun **araç tipi (blade) sigorta** batarya ile devre arasına, XT60'tan hemen sonra takılır. Ana kesme kolaylık içindir; RL3-4 anahtarın etiketindeki **T85 sıcaklık değeridir, DC akım değil** — DC rating doğrulanmadan ana hat anahtarı sayılmaz.
- **Kesit uyarısı:** 18–20 AWG yalnız **servo dalı** için yeterlidir. Batarya → regülatör ana hattı **≥16 AWG (tercihen 14 AWG)** olmalı. Sigorta kablo kesitine göre seçilir: 16 AWG hatta 15–20 A, 14 AWG hatta 25–30 A; sigorta kablodan zayıf olmaz.

Bunlar tamamlanmadan "kurulum bitti" denemez; yalnız tek servo / tek bacak masaüstü testleri yapılabilir.
