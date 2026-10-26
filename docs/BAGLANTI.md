# RoboCat — parça listesi ve bağlantı şablonu

Bu belge **bağlantı şablonudur**, doğrulanmış şematik değildir. Pinler öneridir; modül seviyeleri, pull-up ve gerçek pin dizilimi fiziksel kontrol bekler.

Ana sipariş/teslim/test listesi: [KURULUM.md](KURULUM.md#sipariş-ve-kabul-takibi--2026-10-26). 2× TCA9548A, 2× XL4016, 2× PWM hız kontrolü, 2× voltmetre, 1× sis yapıcı ve 1× PIR **teslim alındı (2026-10-26)**; adet/elektriksel test teyidi yok.

## 1) Parça listesi — durum

[1:1 ölçekli donanım kataloğu](images/robocat-hardware-catalog.svg) · [baskı parçaları kataloğu](GALLERY.md)

### Var (envanterde)
| Grup | Parça | Adet | Not |
|---|---|---:|---|
| Kontrol | Arduino Mega 2560 R3 (CH340) | 1 | Yerel hareket |
| Sürücü | PCA9685 16 kanal I²C PWM | 1 | **16 kanal tamamen dolu** (12 bacak + 4 kol) |
| Servo | MG996R 180° metal dişli | 16 | 12 bacak + 4 kol adayı |
| IMU | GY-521 / MPU6050 | 2 | Biri gövde, biri opsiyonel |
| Mesafe | HC-SR04 | 5 | 2 ön, 1 arka, 2 opsiyonel |
| Görüş | ESP32-CAM + OV2640 | 3 | 2 kafa + 1 kol (Wi-Fi) |
| Haberleşme | HC-06 Bluetooth Classic | 1 | PS2 yerine |
| Gösterge | 16×2 I²C LCD | 1 | Firmware OLED bekliyor (fark) |
| Akım | ACS712 ±30 A | 1 | Toplam akım |
| Sensör | APDS-9930, mikrofon, alev, MQ-8/MQ-214/MQ-3, DHT22, QRE1113 ×4, load cell, nabız, LDR | 1+1+1+3+1+4+1+1+1 | Deney; kalibrasyon yok |
| Güç | Tinylab 3S 2200 mAh 40C LiPo | 2 | Biri yedek (robot kapalıyken) |
| Anahtar | RL3-4 aç/kapa | 1 | DC akım değeri doğrulanacak |
| Rulman | 625 · 5×16×5 mm | — | Temin edildi (2026-10-26); adet sayımı ve cep uyumu testi bekliyor |
| I²C çoklayıcı | TCA9548A | 2 | Teslim alındı (2026-10-26); kanal/firmware testi bekliyor |
| Regülatör | XL4016 düşürücü | 2 | Teslim alındı (2026-10-26); 5 V / 6 V yük testi bekliyor |
| Sarf | PETG beyaz + metalik (1,75 mm) | 2 | Baskı malzemesi |

### Eksik / alınacak
| Parça | Ölçü / sınıf | Neden |
|---|---|---|
| 6 V servo regülatörü | ≥15–20 A sınıfı, termal değerlendirilecek | 12 servo stall'da 25–30 A çekebilir |
| 5 V regülatör | 2× XL4016 teslim alındı; yük/ısınma testi bekliyor | Ayrı elektronik hattı adayı |
| DC sigorta + yuva | Hat akımına göre | Yangın/kısa devre |
| LiPo düşük gerilim alarmı/koruması | 3S | Hücre başına ≥3,5 V uyarı |
| Balanslı şarj cihazı | 3S | (varsa doğrulanmadı) |
| 25T alüminyum horn | **10,0 mm** (ikincil 13,9 mm) delik deseni | Ölçüldü; horn kalınlığı doğrulanacak |
| Vida/somun | M3×8–10, M4×10–12, somun, pul | M3 geçiş Ø3,0–3,4; pilot Ø2,4–2,9 |
| Servo uzatma | 3-pin ×12 | Kablolama |
| HX711 | — | Load cell için |
| XT60 + yüksek akım kablo | 18–20 AWG | (varsa doğrulanmadı) |

### Basılmayacak
CAT10 kızak · BAT01 kartuş kapağı · eski 18650 kasetleri · doğrulanmamış omuz ultrasonik braketi.

## 2) Mega 2560 bağlantı matrisi

| Mega pini | Modül | Sinyal | Durum |
|---|---|---|---|
| D20 / D21 | PCA9685 | SDA / SCL | Öneri |
| D8 | PCA9685 | OE (enable) | Öneri |
| D18 (TX1) / D19 (RX1) | HC-06 | Mega TX → HC-06 RX, Mega RX ← HC-06 TX | Seviye dönüşümü kontrol |
| D2 / D3 | MPU6050 ×2 | INT | Opsiyonel |
| D4 | DHT22 | DATA | Pull-up |
| D5 | Alev sensörü | DO | Polarite TBD |
| D6 / D7 | HX711 | DT / SCK | Modül yok |
| D22 | APDS-9930 | INT | — |
| D34–D39 | HC-SR04 ×3 | TRIG/ECHO (ön-sol, ön-sağ, arka) | 5 V |
| D40–D43 | HC-SR04 ×2 | Opsiyonel | — |
| A0–A2 | MQ-8 / MQ-3 / MQ-214 | AO | Isıtıcı beslemesi ayrı |
| A3 | Mikrofon | AO | — |
| A4 | LDR | Bölücü | Direnç gerekir |
| A5 | Nabız sensörü | AO | Opsiyonel |
| A6 | ACS712 | AO | 5 V referans kalibrasyonu |
| A8–A11 | QRE1113 ×4 | Fototransistör | Okuma devresi gerekir |
| D24–D27 | *(PS2 alıcı — bizde yok)* | DAT/CMD/SEL/CLK | HC-06 ile kullanılmaz |

## 3) PCA9685 kanal haritası

Firmware `servoSetup` dizisi (sürücü 1):

| Kanal | Servo | Bacak | Görev |
|---:|---|---|---|
| 0 | RFC | Sağ ön | Coxa (abduction) |
| 1 | RFF | Sağ ön | Femur |
| 2 | RFT | Sağ ön | Tibia |
| 3 | **boş** | — | Kol adayı |
| 4 | LFC | Sol ön | Coxa |
| 5 | LFF | Sol ön | Femur |
| 6 | LFT | Sol ön | Tibia |
| 7 | **boş** | — | Kol adayı |
| 8 | RRC | Sağ arka | Coxa |
| 9 | RRF | Sağ arka | Femur |
| 10 | RRT | Sağ arka | Tibia |
| 11 | **boş** | — | Kol adayı |
| 12 | LRC | Sol arka | Coxa |
| 13 | LRF | Sol arka | Femur |
| 14 | LRT | Sol arka | Tibia |
| 15 | **boş** | — | Kol adayı |

**Sonuç:** tek PCA9685 16 kanalıyla 12 bacak + 4 kol sığar; TCA9548A şart değil **ama** firmware `tca_select()` çağırıyor → kodda stub/sadeleştirme gerekir.

## 3b) Rulman uyumu — 625 (5×16×5)

Güncel sette ölçülen (`SM3_Frame_FrontShoulderMiddle`, `SM3_Frame_LeftFemur`, `SM3_Frame_LeftTibia`):

| Özellik | Ölçüm | Sonuç |
|---|---|---|
| Dış yuva çapı | Ø15,9–16,3 mm | 625 (Ø16) oturur |
| Mil / geçiş delikleri | Ø5,0–5,5 mm | 625'in Ø5 iç çapı ve Ø5 mil ile uyumlu |
| Yuva (yatak) derinliği | **≈3,6–4,0 mm** | 5 mm geniş rulman ~1 mm dışarıda kalır; gerekirse cep 5,2 mm'ye açılır |
| 8 mm delik | **bulunmadı** | Tasarım zaten Ø5 mil kullanıyor; geometri değişikliği gerekmiyor |

Not: `Nova-SM2` BOM'undaki "8×16×5" ifadesi SM3 geometrisiyle uyuşmuyor; SM3 parçaları Ø5 mil için modellenmiş. **625 seçimi doğru.** Ölçümler kesit tabanlıdır; baskı sonrası gerçek geçme denenmeli.

## 4) Güç yolu

```
3S LiPo 11,1 V (12,6 V dolu) → XT60 → sigorta → ana kesme
   ├── 6 V regülatör → servo barası (PCA9685 V+) → 16 servo
   └── 5 V regülatör → Mega 5V, HC-06, LCD, sensörler
```

| Kural | Açıklama |
|---|---|
| LiPo → servo | **Asla doğrudan**; 4,8–7,2 V servo aralığı |
| Kesit | Servo hattı 18–20 AWG, ortak GND tek noktada |
| Breadboard | Servo gücü için kullanılmaz |
| USB + harici | Aynı anda ters besleme yapılmayacak |
| PCA9685 V+ | Ayrı servo barasından; VCC mantığı 5 V |

## 5) Firmware uyumsuzlukları (kurulumdan önce)

| Konu | Firmware | Bizde | Yapılacak |
|---|---|---|---|
| I²C mux | TCA9548A | 2 teslim alındı (2026-10-26) | Kanal/adres kontrolü; tek PCA9685 uyarlaması |
| Kumanda | PS2 alıcı | HC-06 | Serial1 komut katmanı |
| Gösterge | OLED (SSD1306/SSD1331) | 16×2 I²C LCD | LCD sürücüsü |
| Servo | DS3218 270° varsayımı | MG996R 180° | `servoHome`/`servoLimit` yeniden |

Şema görseli: [bağlantı şeması](images/robocat-wiring.svg) · mimari: [SYSTEM.md](SYSTEM.md) · güç: [PCB_PLAN_REV_A.md](../hardware/PCB_PLAN_REV_A.md)
