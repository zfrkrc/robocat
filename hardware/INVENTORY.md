# RoboCat — satın alınan parça envanteri

> **Güncel batarya kararı (2026-10-25):** Tek Tinylab 3S 11.1 V 2200 mAh 40C LiPo hedefleniyor; 108×35×21 mm, XT60. Satın alındığı/adedi henüz doğrulanmadı. Hot-swap iptal, yedek pil robot kapalıyken değiştirilir. Aşağıdaki 18650 yuvası satın alınmış envanter olarak korunur ama güncel bataryada kullanılmaz; iki 3S kartuş/hot-swap için eski eksik listesi artık güncel mimari değildir. Sigorta, regülasyon ve LiPo düşük hücre gerilimi koruması hâlâ gerekli. Güncel güç planı PCB_PLAN_REV_A.md içindeki rev B'dir.

Tarih: 2026-10-26. Kaynak: kullanıcının paylaştığı sipariş listesi. Adetler fiziksel sayım veya fotoğrafla doğrulanmadı. İki ayrı MG996R satırı 12+4=16, iki ayrı GY-521 satırı 1+1=2 olarak birleştirildi. Fiyatların satır toplamı/birim ayrımı kesin olmadığı için toplam maliyet hesaplanmadı. Sipariş listesindeki isimler gerçek PCB boyutunu ve pin dizilimini doğrulamaz.

## Elektronik ve hareket
| Parça | Adet | Planlanan kullanım / durum |
|---|---:|---|
| Arduino Mega 2560 R3 klon, CH340, USB kablolu | 1 | Ana yürüyüş kontrolcüsü; standart Mega R3 formu olarak sipariş edilmiş |
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

## İlk aşama — seçilen ana set
Mega + 12 MG996R + PCA9685 + bir GY-521 + iki ön HC-SR04 + HC-06 + LCD. İlk tek-servo denemesinde doğrulanmış haricî regüle besleme ve ortak GND kullanılacak. Kamera ve gaz sensörleri yürüyüş doğrulanınca eklenir. Kalan dört MG996R kol için ayrılır; bu ayrım mevcut kolun üretime hazır olduğu anlamına gelmez.

## Güncel eksikler / doğrulanacaklar — tek LiPo
- Tinylab 3S 2200 mAh 40C LiPo hedefi netleşti; satın alma/adedi fiziksel teyit edilmedi. 18650 hücreler ve ikinci üçlü yuva artık bu mimarinin gereksinimi değildir.
- Uygun 3S LiPo balanslı şarj, düşük hücre gerilimi izleme/koruma çözümü, DC sigorta ve uygun ana kesme.
- 2× XL4016 sipariş edildi: 5 V elektronik ve 6 V tek-bacak test hattına aday. Teslim/yük/ısınma testi bekleniyor; bütün robot için yüksek akım kapasitesi onaylanmadı.
- Yüksek akım kablo/konnektör/dağıtım, servo uzatma ve güvenilir ortak GND.
- **Rulman seçimi: 625 (5×16×5).** Güncel `SM3_Frame_*` setinde kesitle ölçülen: dış yuva Ø15,9–16,3 mm, mil/geçiş delikleri Ø5,0–5,5 mm, yuva derinliği ≈3,6–4,0 mm; 8 mm delik bulunmadı. Yani SM3 geometrisi Ø5 mil için modellenmiş; 625 uyumlu, baskı sonrası gerçek geçme ve 5 mm'lik rulman için cep derinliği (gerekirse ream) doğrulanacak.
- Mekanik modele uygun vida, somun, servo hornu ve rulmanlar; gerçek MG996R ile tek yuva denemesi.
- Load cell için HX711 veya uygun yükselteç/ADC; çıplak QRE/LDR için okuma devresi.
- Modül pinleri, lojik seviyeler, PCB/gövde ölçüleri. Satın alma listesi fiziksel uyumu doğrulamaz.
- Hot-swap iptal. İki bağımsız kartuş, iki BMS ve hot-swap devresi artık sipariş listesine otomatik eklenmez; tek LiPo'nun koruma gereksinimi ayrıca tasarlanacak.

## Burun tasarımına etkisi
MQ sensörleri mevcut kedi burnuna doğrudan yerleştirilmeyecek. Örneğin Winsen MQ-8 5 V ısıtıcı kullanır ve üretici belgesinde ısıtıcı tüketimi 950 mW'a kadar belirtilir. Havalandırmalı, ısıl ayrımı olan ayrı sensör bölmesi ve besleme bütçesi gerekir. Üç farklı gaz sensörü genel koku tanıma ya da koku izini takip etme yeteneğini otomatik sağlamaz. Ölçümler kalibrasyonsuz ppm/güvenlik alarmı olarak sunulmayacak.

Kaynaklar:
- APDS-9930 üretici veri sayfası: https://docs.broadcom.com/wcs-public/products/data-sheets--technical-specifications/data-sheet/736/749/av02-3190en_ds_apds-9930_2015-11-13.pdf
- MQ-8 üretici veri sayfası: https://www.winsen-sensor.com/d/files/manual/mq-8.pdf

Bu güncelleme yalnız envanter belgesidir; baskı kuyruğu, STL, G-code veya yazıcı ayarı değiştirilmedi.



## Sipariş ve kabul takibi — 2026-10-26

Ana izleme yeri bu kurulum klasörüdür. **Sipariş verildi ≠ teslim alındı ≠ test edildi.** Aşağıdaki yeni siparişlerin teslimi ve fiziksel kabulü henüz teyit edilmedi.

| Parça | Sipariş | Teslim alınan | Test edilen | Kullanım / sonraki adım |
|---|---:|---|---|---|
| TCA9548A I²C çoklayıcı | 2 | Teyit bekliyor | 0 | 1 kullanım + 1 yedek; kanal/adres eşlemesi firmware ile doğrulanacak |
| PWM DC motor hız kontrolü 1,8–12 V / 2 A | 2 | Teyit bekliyor | 0 | Servo regülatörü değildir; dolu 3S (12,6 V) doğrudan bağlanmaz |
| Dijital DC voltmetre, kırmızı | 2 | Teyit bekliyor | 0 | Batarya ve 6 V hattı göstergesi adayı; hücre koruması değildir |
| USB 5 V ultrasonik sis yapıcı | 1 | Teyit bekliyor | 0 | Sonraki efekt aşaması; ilk yürüyüşe dahil değil |
| HC-SR501 PIR | 1 | Teyit bekliyor | 0 | Opsiyonel hareket algılama; pin tahsisi henüz yok |
| XL4016 düşürücü regülatör, Robo90 200W başlıklı | 2 | Teyit bekliyor | 0 | Bir kart 5 V elektronik, bir kart 6 V tek-servo/tek-bacak testine aday |

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
