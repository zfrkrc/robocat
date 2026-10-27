# Çevre sensör düğümü — ESP32 bağlantı şeması

![ESP32 çevre sensör düğümü bağlantı şeması](images/env-node-wiring.svg)

*Blok seviyesi şema. Pin dizilimi kart üzerindeki etiketle doğrulanmalıdır.*

## Amaç

Hasta odası / atölye için kamerasız ortam izleme: alkol, metan, hidrojen, nabız, sıcaklık-nem ölçümü; 16×2 LCD'de özet, web arayüzünde canlı değerler. Müzik ve anons sesleri ayrı hat üzerinden.

## Kart

| | |
|---|---|
| Kart | **ESP32-D0WDQ6** (ESP8266 değil), 4 MB flash, CP2102 USB |
| MAC | `80:7d:3a:99:85:e8` |
| Firmware | `env-node` v0.2.4 |
| Ağ | `maske` WiFi → **172.16.16.232** (DHCP; IP değişebilir), mDNS `env-node.local` |
| Web | `http://172.16.16.232/` · `/api` · `/sweep` · `/tare` · `/lcd` |
| Durum | Kart bağlı; MQ-3/MQ-214/MQ-8 ve HX711 görünüyor. DHT22 okunamıyor, LCD I²C'de bulunamıyor |

> Not: Bu kart ilk bakışta ESP8266 sanıldı; `esptool` ESP32-D0WDQ6 olduğunu doğruladı. A2DP + I²S + çok kanallı ADC yalnız ESP32'de var, bu yüzden proje bu kartla ilerliyor.

## Pin tablosu

| İşlev | Sensör / modül | ESP32 pini | Not |
|---|---|---|---|
| Alkol | MQ-3 AOUT | **GPIO32** (ADC1) | 5 V besleme + 10k/10k bölücü |
| Metan | MQ-214 AOUT | **GPIO33** (ADC1) | Bölücü |
| Hidrojen | MQ-8 AOUT | **GPIO34** (ADC1) | Bölücü, ısıtıcı ~950 mW |
| Nabız | Sensör S | **GPIO35** (ADC1) | 3,3 V, bölücü yok |
| Sıcaklık/nem | DHT22 DATA | **GPIO4** | 10k pull-up · şu an okunamıyor |
| LCD | SDA / SCL | **GPIO21 / GPIO22** | VCC 5 V, adres 0x27 veya 0x3F |
| Ses (I²S) | MAX98357A BCK / LRC / DIN | **GPIO26 / 25 / 27** | VIN 5 V, hoparlör 4–8 Ω |
| Ağırlık | HX711 DT / SCK | **GPIO18 / GPIO19** | Load cell; kalibrasyon (scale) gerekir |
| Yerel MP3 (ops.) | DF1201S TX / RX | **GPIO17 / 16** | SD'den uyarı/anons sesleri |

**ADC kuralı:** MQ sensörlerinin AOUT çıkışı 5 V'a kadar çıkabilir; ESP32 ADC'si **3,3 V** kabul eder. Her MQ hattına **10k/10k gerilim bölücü** konur (çıkış = AOUT/2). Ayrıca **ADC2 (GPIO0–15) WiFi açıkken kullanılamaz**, bu yüzden tüm analog girişler ADC1'dedir.

## Güç

| Yük | Akım |
|---|---|
| 3× MQ ısıtıcı | ~450 mA sürekli |
| ESP32 | 240 mA tepe |
| LCD + DHT | ~25 mA |
| MAX98357A + hoparlör | 0,5–2 A tepe |

**5 V / 3 A** adaptör, tek nokta ortak GND, MQ ısıtıcıları için ayrı 5 V dalı.

## Kart etiketleri — D21 / TX0 karışıklığı

| Kart etiketi | GPIO | Kullanım |
|---|---|---|
| **D21** | GPIO21 | I²C **SDA** (LCD) |
| **D22** | GPIO22 | I²C **SCL** (LCD) |
| TX0 | GPIO1 | USB seri TX — **sensöre bağlanmaz** |
| RX0 | GPIO3 | USB seri RX — **sensöre bağlanmaz** |
| D32 / D33 / D34 / D35 | ADC1 | MQ-3 / MQ-214 / MQ-8 / nabız |

## LCD sorun giderme

Ekranda anlamsız harfler/bloklar = LCD **initialize edilmemiş** (I²C konuşmuyor). Sıra:

1. LCD arkasındaki **I²C backpack** var mı? (16 pinli çıplak LCD ise I²C dönüştürücü gerekir.)
2. 4 kablo: **VCC 5 V · GND · SDA → D21 · SCL → D22** (SDA/SCL ters olabilir, cihaz ikisini de dener).
3. `GET /sweep` → 4 olası pin çiftinde I²C taraması yapar, `/sweep/status` sonucu verir.
4. Cihaz hâlâ `lcd: yok` diyorsa kablo/lehim veya backpack arızası; kontrast potu yalnız görünürlüğü etkiler, karakter bozukluğunu çözmez.

## Şu anki okumalar (2026-10-27)

| Sensör | Durum |
|---|---|
| MQ-3 alkol | ✅ ~560 mV (sensör bağlı) |
| MQ-214 metan | ✅ ~395 mV |
| MQ-8 hidrojen | ✅ ~270 mV |
| Nabız | ⚠️ 0 mV (parmak yok) |
| DHT22 | ❌ okunamıyor (GPIO4'te veri yok) |
| HX711 | ✅ çip yanıt veriyor, ağırlık 0 g (load cell/kalibrasyon?) |
| LCD | ❌ I²C'de bulunamadı |

## Sensör gerçekleri

- MQ serisi **kalibrasyonsuz ppm iddia etmez**; panelde 0–1 normalize indeks gösterilir.
- MQ'lar **24–48 saat burn-in**, her açılışta **5–10 dk ısınma** ister.
- Nabız sensörü hobi amaçlıdır, tıbbi cihaz değildir.
- Metan/alkol ölçümü güvenlik sertifikası yerine geçmez; alarm senaryosu ayrıca tasarlanmalı.

## Ses mimarisi

| Mod | Yöntem | Durum |
|---|---|---|
| Müzik | Telefon/PC → **Bluetooth A2DP** → ESP32 → MAX98357A | Planlı (ESP32 Classic BT) |
| Yerel ses | DF1201S + SD kart (uyarı, zil, anons) | Opsiyonel |
| Otomatik akış | Sunucuda yt-dlp → HTTP MP3 → I²S | Sonraki aşama, kırılgan |

## Uçlar

| Uç | İçerik |
|---|---|
| `/` | Canlı kartlar (mV, raw, RSSI, heap) |
| `/api` | JSON: `adc[]`, `rssi`, `heap`, `uptime`, `i2c`, `lcd` |

## Sıradaki adımlar

1. LCD'yi bağla (SDA 21 / SCL 22) → I²C taraması adresi bulsun, ekran sayfaları açılsın.
2. MQ-3 / MQ-214 / MQ-8 + bölücüleri bağla → ham mV doğrula.
3. DHT22 ve nabız sensörünü ekle.
4. Kalibrasyon: boş oda baseline, sensör başına eğri.
5. Bluetooth A2DP hoparlör modu + panelden ses kontrolü.
6. İsteğe bağlı: `robocat.zk.net.tr`ye `role=other`, `capabilities=["env_sensor"]` ile event gönderimi.

## Kaynak

Yerel proje: `/root/env-node` (PlatformIO, `esp32dev`). Şema: `docs/images/env-node-wiring.svg`.
