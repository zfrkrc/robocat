# RoboCat — satın alınan parça envanteri

> **Güncel batarya kararı (2026-10-25):** Tek Tinylab 3S 11.1 V 2200 mAh 40C LiPo hedefleniyor; 108×35×21 mm, XT60. Satın alındığı/adedi henüz doğrulanmadı. Hot-swap iptal, yedek pil robot kapalıyken değiştirilir. Aşağıdaki 18650 yuvası satın alınmış envanter olarak korunur ama güncel bataryada kullanılmaz; iki 3S kartuş/hot-swap için eski eksik listesi artık güncel mimari değildir. Sigorta, regülasyon ve LiPo düşük hücre gerilimi koruması hâlâ gerekli. Güncel güç planı PCB_PLAN_REV_A.md içindeki rev B'dir.

Tarih: 2026-10-26. Kaynak: kullanıcının paylaştığı sipariş listesi. Adetler fiziksel sayım veya fotoğrafla doğrulanmadı. İki ayrı MG996R satırı 12+4=16, iki ayrı GY-521 satırı 1+1=2 olarak birleştirildi. Fiyatların satır toplamı/birim ayrımı kesin olmadığı için toplam maliyet hesaplanmadı. Sipariş listesindeki isimler gerçek PCB boyutunu ve pin dizilimini doğrulamaz.

## Elektronik ve hareket
| Parça | Adet | Planlanan kullanım / durum |
|---|---:|---|
| Arduino Mega 2560 R3 klon, CH340, USB kablolu | 1 | Ana yürüyüş kontrolcüsü; standart Mega R3 formu olarak sipariş edilmiş. **Fiziksel/USB teyidi yok** (2026-10-26: CH340 portu görünüyor ama avrdude sync 12/12 başarısız) |
| MG996R 180 derece servo | 16 | 12 bacak, kalan 4 kol için aday; kol torku/kinematiği henüz doğrulanmadı |
| PCA9685 16 kanal I²C PWM/servo sürücü shield | 1 | Önce 12 bacak sinyali. Shield mi bağımsız modül mü fotoğrafla doğrulanmalı. VCC ile servo V+ ayrılmalı |
| GY-521 / MPU6050 | 2 | Bir gövde IMU'su; ikincisi yedek/kol için opsiyonel. İkisi aynı I²C hattındaysa adres düzeni gerekir |
| HC-SR04 ultrasonik | 5 | İki ön/sabit omuz, bir arka; kalan iki opsiyonel. Sırayla ölçüm |
| ESP32-CAM + OV2640, TLS Robotik | 3 | İki sabit kafa, bir kol kamerası |
| HC-06 Bluetooth | 1 | Manuel kontrol; Bluetooth Classic, BLE olarak varsayılmayacak |
| 16x2 I²C LCD mavi | 1 | Durum / batarya / hata gösterimi |
| ACS712 +/-30 A kart | 1 | Toplam akım izlemesine aday; kart terminal/iz akım kapasitesi ayrıca doğrulanacak. Tek sensör iki kartuşu bağımsız ölçmez |
| RL3-4 iki pin aç/kapa anahtar | 1 | Akım/DC etiketine göre kontrol veya uygun güç anahtarlaması; T85 ibaresi akım değeri değildir |
| Üçlü 18650 PCB tipi altı pin pil yuvası | 1 | Tek üçlü yuva. Bağlantı/topoloji ve akım kapasitesi doğrulanmadı; otomatik 3S BMS'li kartuş kabul edilmez |
| 120 parça, 100 mm jumper kablo seti | 1 set | Sinyal/deneme bağlantısı; servo yüksek akım dağıtımı için kullanılmayacak |
| HC-SR04 montaj aparatı Tip C | 1 | Tek sensör için; mekanik ölçüsü bilinmiyor |

Daha önce elinde olduğu belirtilen ESP32-C3 ve ESP8266 kartları da var; adet/model henüz belirtilmedi. Bu sipariş listesinde yeniden satın alınmış sayılmadılar.

## Ek sensörler
| Parça | Adet | Kullanım / sınır |
|---|---:|---|
| CJMCU-9930 / APDS-9930 | 1 | Yakınlık + ortam ışığı; hareket yönü/jest sensörü veya 1 m takip mesafesi sensörü değildir |
| Mikrofon / ses sensör kartı | 1 | Ses seviyesi/eşik denemesi; anlaşılır ses kaydı ve konuşma tanıma desteği kart devresine bağlı, varsayılmıyor |
| Ateş algılayıcı sensör kartı | 1 | Optik alev algılama denemesi; sertifikalı yangın güvenlik sistemi değildir |
| MQ-8 hidrojen gaz sensör kartı | 1 | Gaz ölçüm denemesi; ısıtıcı/kalibrasyon gerekir |
| MQ-214 metan/yanıcı gaz sensörü | 1 | Sipariş adı bu; çıplak sensör/modül ve kesin model etiketi doğrulanacak |
| MQ-3 alkol gaz sensör kartı | 1 | Gaz ölçüm denemesi; ısıtıcı/kalibrasyon gerekir |
| DHT22 sıcaklık/nem modülü | 1 | Ortam ölçümü; gaz sensörü ısıtıcısından uzağa konulacak |
| QRE1113GR fototransistör çıkışlı sensör | 4 | Yakın yansıma denemesi; ayak zemin/yüzey algılaması için aday. Çıplak parça ise direnç/okuma devresi gerekir; temas/kuvvet sensörü sayılmaz |
| Load cell ağırlık sensörü | 1 | Kapasitesi/tipi belirsiz; HX711 veya uygun ölçüm yükselteci listede yok |
| Parmak nabız sensörü | 1 | Ayrı deney parçası; robot yürüyüşü için gerekli değil, tıbbi ölçüm cihazı değildir |
| 5 mm LDR | 1 | Basit ışık ölçümü; direnç bölücü gerekir |

## Montaj araçları ve sarf
| Parça | Adet |
|---|---:|
| Tassol kurşunsuz krem lehim, sipariş yazımı Sn99Cu07Ag0,3, 50 g | 1 |
| Soldex SR-33 No Clean sıvı flux 250 ml | 1 |
| Felder Löttechnik lehim pastası 50 g | 1 |
| A4 koyu yeşil tamir/kesim matı | 1 |
| Proskit SN-394 büyüteçli/mıknatıslı tutacak | 1 |

Felder ürününün elektronik lehimlemeye uygunluğu ve kalıntı temizleme koşulları ambalaj/teknik bilgiyle doğrulanmalı. Kesim matı ısıya dayanıklı lehim matı varsayılmamalı. Havya/reflow ekipmanı bu listede bulunmuyor; kullanıcıda ayrıca olabilir.

## Fotoğrafla görülen, envanter dışı parçalar — 2026-10-26

Aynı gün paylaşılan 20 fotoğraf ([albüm](../docs/BUILD_PHOTOS_2026-10-26.md)) sipariş listesinde olmayan parçaları da gösteriyor. Bunlar adet/teslim teyidi sayılmaz ve RoboCat BOM'una eklenmez:

| Parça | Fotoğraf | Durum |
|---|---|---|
| **HW-373 V1.2** 1S Li-ion şarj + 5 V boost modülü | IMG_9230 | Geliştirme kartı değil. **1S** girişli; 3S LiPo planında kullanılmaz. Yalnız tek hücre masaüstü denemesi |
| **T413** LDS/taret kartı | IMG_9238 | Robot süpürgeden sökülmüş lazer tarayıcı kartı; pinout bilinmiyor, RoboCat'te işlevi yok |
| Dreame BLDC motor (019-200330 ZD / PRI-3605U-15260) | IMG_9248, IMG_9251 | **Servo değil.** PCA9685 servo sinyaliyle veya basit DC sürücüyle çalışmaz; 3 fazlı sürücü + Hall/enkoder + kapalı çevrim gerekir. Bacak eklemi için uygun değil |
| Dreame `MOTOR_CONN_B0_v2` bağlantı kartı | IMG_9252, IMG_9253 | Süpürge motor/fırça bağlantı kartı; BOM dışı |
| Süpürge redüktörü | IMG_9254–IMG_9256 | Mekanik inceleme parçası; RoboCat bacak/kol redüktörü değil |

Fotoğraflarda **Arduino Mega görünmüyor.** Mega'nın USB teşhisi için [fotoğraf albümündeki 2026-10-26 notuna](../docs/BUILD_PHOTOS_2026-10-26.md#arduino-ve-usb-seri-durumu--2026-10-26) bakın.

## İlk aşama — seçilen ana set
Mega + 12 MG996R + PCA9685 + bir GY-521 + iki ön HC-SR04 + HC-06 + LCD. İlk tek-servo denemesinde doğrulanmış haricî regüle besleme ve ortak GND kullanılacak. Kamera ve gaz sensörleri yürüyüş doğrulanınca eklenir. Kalan dört MG996R kol için ayrılır; bu ayrım mevcut kolun üretime hazır olduğu anlamına gelmez.

## Güncel eksikler / doğrulanacaklar — tek LiPo

Son güncelleme: 2026-10-26 (kargo teslimi ve 625 rulman temini işlendi).

### Hâlâ satın alınacak
| Parça | Not |
|---|---|
| Tinylab 3S 2200 mAh 40C LiPo (veya eşdeğeri) | Hedef model netleşti; satın alma/adedi fiziksel teyit edilmedi. 18650 hücreler ve ikinci üçlü yuva bu mimarinin gereksinimi değil |
| 3S balanslı LiPo şarj cihazı | (varsa marka/model doğrulanmadı) |
| LiPo düşük gerilim alarmı/koruması | 3S; hücre başına ≥3,5 V uyarı |
| DC sigorta + yuva, uygun ana kesme | RL3-4 anahtarın DC akım değeri etiketten doğrulanacak |
| 6 V / ≥15–20 A servo regülatörü | 12 servo stall'da 25–30 A çekebilir; 2× XL4016 (8 A) bu iş için **onaylı değil**, yalnız tek bacak testine aday |
| XT60 + 18–20 AWG yüksek akım kablo, dağıtım klemensi | Ortak GND tek noktada |
| 25T alüminyum servo horn | Delik deseni **10,0 mm** (ikincil 13,9 mm); horn kalınlığı doğrulanacak |
| M3×8–10, M4×10–12 vida, somun, pul | M3 geçiş Ø3,0–3,4; pilot Ø2,4–2,9 |
| 3-pin servo uzatma ×12 | Kablo ekleme değil, hazır uzatma tercih edilecek |
| HX711 | Load cell için; yükselteç/ADC alternatifi de olur |

### Teslim alındı — test veya kod işi bekliyor
| Parça | Kalan iş |
|---|---|
| 2× TCA9548A | Kanal taraması ve firmware kanal eşlemesi (`tca_select`) |
| 2× XL4016 | Yüksüz 5,0 / 6,0 V ayarı, yük altında gerilim–akım–sıcaklık kaydı |
| 2× PWM DC hız kontrolü, 2× voltmetre, 1× sis yapıcı, 1× PIR | Kabul testi; voltmetreler multimetreyle karşılaştırılacak |
| **625 rulman (5×16×5)** | Cep derinliği ≈3,6–4,0 mm; geçme testi, gerekirse cep 5,2 mm'ye ream |
| Arduino Mega 2560 R3 | USB'de CH340 görünüyor ama avrdude sync yok; PWR/TX/GND kontrolü ile fiziksel teyit |

### Ayrıca doğrulanacak
- Yüksek akım kablo/konnektör/dağıtım, servo uzatma ve güvenilir ortak GND.
- Mekanik modele uygun vida, somun ve servo hornu; gerçek MG996R ile tek yuva denemesi.
- Çıplak QRE/LDR için okuma devresi; modül pinleri, lojik seviyeler, PCB/gövde ölçüleri.
- Hot-swap iptal: iki bağımsız kartuş, iki BMS ve hot-swap devresi sipariş listesine otomatik eklenmez; tek LiPo'nun koruma gereksinimi ayrıca tasarlanacak.

## Burun tasarımına etkisi
MQ sensörleri mevcut kedi burnuna doğrudan yerleştirilmeyecek. Örneğin Winsen MQ-8 5 V ısıtıcı kullanır ve üretici belgesinde ısıtıcı tüketimi 950 mW'a kadar belirtilir. Havalandırmalı, ısıl ayrımı olan ayrı sensör bölmesi ve besleme bütçesi gerekir. Üç farklı gaz sensörü genel koku tanıma ya da koku izini takip etme yeteneğini otomatik sağlamaz. Ölçümler kalibrasyonsuz ppm/güvenlik alarmı olarak sunulmayacak.

Kaynaklar:
- APDS-9930 üretici veri sayfası: https://docs.broadcom.com/wcs-public/products/data-sheets--technical-specifications/data-sheet/736/749/av02-3190en_ds_apds-9930_2015-11-13.pdf
- MQ-8 üretici veri sayfası: https://www.winsen-sensor.com/d/files/manual/mq-8.pdf

Bu güncelleme yalnız envanter belgesidir; baskı kuyruğu, STL, G-code veya yazıcı ayarı değiştirilmedi.



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

- [ ] Kargo teslimi, gerçek adet ve kart fotoğrafları kaydedildi
- [ ] XL4016 model/pin/polarite kontrolü ve yüksüz çıkış ayarı yapıldı
- [ ] 5 V elektronik hattı yük/ısınma testi geçti
- [ ] 6 V tek servo, ardından üç servolu bacak testi geçti
- [ ] TCA9548A kanal taraması ve firmware kanal eşlemesi doğrulandı
- [ ] Voltmetreler multimetreyle karşılaştırıldı
- [ ] Sonuçlara göre bütün robotun servo kaynağı kararı verildi

Sipariş kaynakları: [Robolink TCA9548A](https://www.robolinkmarket.com/tca9548a-i2c-coklayici), [PWM kart](https://www.robolinkmarket.com/pwm-dc-motor-hiz-kontrol-devresi-18-12v-2a), [voltmetre](https://www.robolinkmarket.com/dijital-dc-voltmetre-kirmizi), [sis yapıcı](https://www.robolinkmarket.com/usb-ultrasonik-nem-buhar-yapici-modul-5v-sis-yapici), [PIR](https://www.robolinkmarket.com/hc-sr501-ayarlanabilir-ir-hareket-algilama-sensoru-pir), [XL4016](https://www.robo90.com/xl4016-dc-dc-step-down-dusurucu-voltaj-regulatoru-200w).

Ana durum ve kabul listesi: [Kurulum](../docs/KURULUM.md#sipariş-ve-kabul-takibi--2026-10-26).
