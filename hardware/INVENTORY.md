# RoboCat — satın alınan parça envanteri

Tarih: 2026-10-25. Kaynak: kullanıcının paylaştığı sipariş listesi. Adetler fiziksel sayım veya fotoğrafla doğrulanmadı. İki ayrı MG996R satırı 12+4=16, iki ayrı GY-521 satırı 1+1=2 olarak birleştirildi. Fiyatların satır toplamı/birim ayrımı kesin olmadığı için toplam maliyet hesaplanmadı. Sipariş listesindeki isimler gerçek PCB boyutunu ve pin dizilimini doğrulamaz.

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

## Bu listede görünmeyen / ayrıca doğrulanacaklar
- Altı adet aynı model, uygun deşarj akımlı 18650 hücre; marka/model ve mevcut olup olmadığı bilinmiyor.
- İki bağımsız 3S paket için iki uygun BMS, paket başına sigorta ve uygun 12,6 V CC/CV şarj sistemi.
- İkinci üçlü yuva veya ölçü/akım açısından uygun iki bitmiş kartuş. Mevcut genel pil yuvasının yay/kontakları servo tepe akımına uygun sayılmayacak.
- Servo için 6 V yüksek akım BEC/regülatör; elektronik/kameralar için kararlı ayrı besleme.
- Hot-swap için ters akım engelleme ve ilk takma akımı sınırlaması; sıradan iki soketi doğrudan paralellemek yeterli değil.
- Yüksek akıma uygun güç kablosu, dağıtım, konnektör, servo uzatma kabloları, acil servo güç kesmesi.
- Mekanik sete uygun vida, somun, servo hornları ve rulmanlar.
- Load cell kullanılacaksa uygun yükselteç/ADC, modeline göre seçilecek.
- ESP ve HC-06 gibi 3,3 V lojikli girişler için gerekirse seviye dönüştürücüler/dirençler.
- Motor, kart, pil yuvası, gaz modülü ve sabit gövde ölçüleri. Mevcut envanter STL yuvalarının fiziksel uyumunu onaylamaz.

## Burun tasarımına etkisi
MQ sensörleri mevcut kedi burnuna doğrudan yerleştirilmeyecek. Örneğin Winsen MQ-8 5 V ısıtıcı kullanır ve üretici belgesinde ısıtıcı tüketimi 950 mW'a kadar belirtilir. Havalandırmalı, ısıl ayrımı olan ayrı sensör bölmesi ve besleme bütçesi gerekir. Üç farklı gaz sensörü genel koku tanıma ya da koku izini takip etme yeteneğini otomatik sağlamaz. Ölçümler kalibrasyonsuz ppm/güvenlik alarmı olarak sunulmayacak.

Kaynaklar:
- APDS-9930 üretici veri sayfası: https://docs.broadcom.com/wcs-public/products/data-sheets--technical-specifications/data-sheet/736/749/av02-3190en_ds_apds-9930_2015-11-13.pdf
- MQ-8 üretici veri sayfası: https://www.winsen-sensor.com/d/files/manual/mq-8.pdf

Bu güncelleme yalnız envanter belgesidir; baskı kuyruğu, STL, G-code veya yazıcı ayarı değiştirilmedi.
