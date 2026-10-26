# RoboCat — ilan metni ve görseller

Hedef sayfa: **https://hobby.zaferkaraca.net/products/20** (canlı, 2026-10-26).
> Not: `hobyy.zaferkaraca.net` DNS'te yok; doğru adres **hobby**.zaferkaraca.net.

**Yayın kuralı:** İlan metninde ve görsellerde tutar/ücret bilgisi yer almaz. İlanda yalnız teknik içerik, durum ve iletişim çağrısı bulunur.

Görseller: [`site-upload/`](site-upload) — 8 dosya, en fazla 1600 px genişlik, JPEG.

## Önce düzeltilmesi gerekenler (mevcut ilanda)

| # | Mevcut ifade | Sorun | Öneri |
|---|---|---|---|
| 1 | "12 bacak servosu (MG996R sınıfı)" | Envanterde **16** servo var: 12 bacak + 4 kol | "16× MG996R (12 bacak + 4 kol)" |
| 2 | "kartvizit mekanizması için yaylı kol montajı" | Projede **hedef özellik**, doğrulanmış mekanizma yok | Kit içeriğinden çıkar veya "hedef" olarak yaz |
| 3 | "Lehimlenmiş güç dağıtımı" | Güç bileşenleri henüz seçilmedi/doğrulanmadı | "Güç dağıtımı prototip aşamasında" |
| 4 | "Fiyat için iletişime geçin" | Yayın kuralına aykırı | Satırı kaldır; mevcut "Teklif / bilgi al" düğmesi kalsın |
| 5 | "teslim öncesi her parça test edilir" | Doğrulanmış test kapsamı yok | "Teslim öncesi test kapsamı sipariş sırasında yazılı paylaşılır" |

"Prototip" ibaresi ve "Görsel: konsept render" notu **korunmalı**.

## Başlık

RoboCat — Açık Kaynak Dört Ayaklı Robot (DIY Kiti)

## Kısa açıklama

Kamera görüşü, Bluetooth kumanda ve 16 servolu yürüyüş için açık kaynak dört ayaklı robot kedi projesi; PETG baskı gövde, DIY kit.

## Uzun açıklama (kopyala-yapıştır)

RoboCat, dört ayaklı bir robot kedi projesidir. Gövde ve bacak parçaları PETG ile 3B basılır; kafa için ayrı CAD/STL/STEP seti vardır. Hareket, Arduino Mega 2560 ve 16 kanallı PCA9685 servo sürücüsü üzerinden 12 bacak servosuyla yürütülür; kalan 4 servo kol içindir. Kafada iki ESP32-CAM bulunur ve görüntü Wi-Fi ile merkeze aktarılır; kameralar Mega'ya veri kablosuyla bağlanmaz. HC-06 Bluetooth manuel kumanda, 16×2 I²C LCD durum göstergesi, MPU6050 ve HC-SR04 ultrasonik sensörler planda. Güç tarafı 3S LiPo, 6 V servo ve 5 V elektronik hatları olarak tasarlanıyor.

Proje açık kaynaktır (MIT) ve Chris Locke / cguweb-com Arduino-Projects deposundan forklanmıştır. Nova-SM sürümlerinin kodu bu donanımla birebir uyumlu değildir; HC-06 komut katmanı ve tek PCA9685 yapılandırması uyarlanmalıdır. Depo: github.com/zfrkrc/robocat

**Durum: prototip.** Gövde, güç ve yürüyüş entegrasyonu üzerinde çalışılıyor. Görsellerin bir kısmı konsept veya CAD çıktısıdır; nihai ürün birebir aynı olmayabilir.

## Kit içeriği

- 3B baskı PETG gövde, bacak ve kafa parçaları
- 16× MG996R servo (12 bacak + 4 kol) ve montaj donanımı
- Arduino Mega 2560 + PCA9685 16 kanal servo sürücü
- MPU6050 IMU, HC-SR04 ultrasonik sensörler
- 2× ESP32-CAM (sabit kafa) ve kamera bağlantı parçaları
- HC-06 Bluetooth, 16×2 I²C LCD
- Montaj kılavuzu ve açık kaynak depo erişimi

## Teknik özellikler

| Alan | Değer |
|---|---|
| Gövde | PETG 3B baskı; kafa CAD v0.3 |
| Servo | 16× MG996R (12 bacak + 4 kol adayı) |
| Kontrol | Arduino Mega 2560 R3 + PCA9685 (16 kanal) |
| Algılama | MPU6050, 5× HC-SR04 |
| Görüş | 2× ESP32-CAM, Wi-Fi |
| Haberleşme | HC-06 Bluetooth Classic |
| Gösterge | 16×2 I²C LCD |
| Güç | 3S LiPo; 6 V servo, 5 V elektronik (prototip) |
| Yazılım | Nova-SM3 türevi; MIT lisans |
| Durum | Prototip |

## Görsel sırası ve alt metinler

| Sıra | Dosya | Alt metin |
|---:|---|---|
| 1 | `site-upload/01-konsept.jpg` | Konsept görsel — nihai ürün birebir aynı olmayabilir |
| 2 | `site-upload/02-kafa-cad.jpg` | Kafa CAD v0.3 |
| 3 | `site-upload/03-baski.jpg` | PETG baskı aşaması |
| 4 | `site-upload/04-servo.jpg` | MG996R servo ve çıkış mili |
| 5 | `site-upload/05-esp32-cam.jpg` | ESP32-CAM ve kamera modülü |
| 6 | `site-upload/06-guc-mimarisi.jpg` | Güç mimarisi (plan) |
| 7 | `site-upload/07-kontrol-mimarisi.jpg` | Kontrol ve görüntü mimarisi |
| 8 | `site-upload/08-lipo-tepsisi.jpg` | LiPo tepsisi — boş uyum denemesi |

## Yayınlama durumu

- Sayfa canlı ve tek görselle (`robocat-konsept.jpg`) yayında.
- Bu makineden panele/SSH'e erişim yok: `ssh.zk.net.tr` Cloudflare Access tarayıcı girişi istiyor, site paneli kimlik bilgisi yok.
- Metin ve görseller hazır; panelden yüklenmesi gerekiyor.

## İlgili

- [Proje fotoğrafları](BUILD_PHOTOS_2026-10-26.md)
- [Galeri](GALLERY.md)
- [Envanter](../hardware/INVENTORY.md)
