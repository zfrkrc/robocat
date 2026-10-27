<div align="center">

# RoboCat

**Dört ayaklı robot kedi · yerel hareket · merkezde görüntü işleme**

`Nova-SM3 tabanı` · `16 MG996R` · `3 ESP32-CAM` · `Metalik + beyaz PETG`

[Kurulum ve ilerleme](docs/KURULUM.md) · [Fotoğraflar](docs/BUILD_PHOTOS_2026-10-26.md) · [Baskı merkezi](docs/PRINTING.md) · [Donanım](hardware/INVENTORY.md)

<img src="docs/images/robocat-petg-colors.png" alt="RoboCat metalik ve beyaz PETG parça dağılımı" width="850">

*CAD üzerinden renk ve parça görünümü. Tamamlanmış robot veya başarılı montaj kaydı değildir.*

</div>

---

## Şu anda: masaüstü kurulum ve baskı uyumu

**27 Ekim 2026** · Parçalar toplanıyor, kafa uyumu hazırlanıyor ve elektronik test aşamasına geçiliyor. Yürüyüş, kol ve kamera takibi henüz doğrulanmadı.

| Alan | İlerleme | Sıradaki kontrol |
|---|---|---|
| **Donanım** | 16 MG996R, Mega, PCA9685, 3 kamera, 5 ultrasonik ve 2 IMU kayıtlı | Fiziksel model, pin ve montaj uyumu |
| **Yeni teslimler** | TCA9548A, XL4016, voltmetre, PWM kontrolü, PIR ve sis yapıcı teslimi kurulum kaydına işlendi | Adet/kart kontrolü ve elektriksel kabul |
| **Gövde ve kafa** | Nova-SM3 gövde/bacak seti; kafa STL/STEP kaynakları ve parça katalogları var | Gerçek servo, kamera, horn ve rulmanla kuru montaj |
| **PETG** | Metalik ilk aşama v0.5: altı ayrı tek-parça uyum işi hazır | Makara etiketi, dilimleme ve ilk kupon |
| **Göz çerçevesi** | CAT06B tek birleşik katı olarak düzeltildi | Kamera görüntüsü, görüş açıklığı ve kuru yerleşim |
| **Güç** | 2× 3S LiPo; tek paketle çalışma, ikinci paket yedek. XL4016 kartları teslim kaydında | 5 V elektronik ve 6 V test hattının yük/ısınma kontrolü |
| **Yazılım** | Nova referans firmware'i + ESP8266 köprü iskeleti + cihaz protokolü | Mega yükleme teyidi, HC-06 uyarlaması ve servo kalibrasyonu |
| **Fotoğraf kaydı** | 20 gerçek baskı/donanım fotoğrafı albümde | Yeni montaj ve test sonuçları |
| **PCB** | Mimari ve pin önerileri var | Masaüstü testlerden sonra şematik/PCB; üretim dosyası henüz yok |

**Ana takip belgesi: [Kurulum ve kabul listesi](docs/KURULUM.md).** Teslim alınan parça, testten geçmiş parça sayılmaz. Bu ana sayfa son durumun özetidir; ayrıntılı sonuçlar orada tutulur.

## Atölyeden

<table>
<tr>
<td width="50%" align="center">
<img src="docs/images/build-2026-10-26/img_9220.jpg" alt="Yazıcıdaki kafa parçaları" width="420"><br>
<strong>Baskı aşaması</strong>
</td>
<td width="50%" align="center">
<img src="docs/images/build-2026-10-26/img_9249.jpg" alt="Gerçek MG996R servo" width="420"><br>
<strong>MG996R ile uyum denemeleri</strong>
</td>
</tr>
</table>

[Gerçek proje albümü](docs/BUILD_PHOTOS_2026-10-26.md) · [CAD, katalog ve diyagram galerisi](docs/GALLERY.md)

## Önce metalik PETG

**Güncel ilk aşama: [v0.5 talimatı](custom/petg-stage-v0.5/README.md) · [iş listesi](custom/petg-stage-v0.5/metallic_queue.json)**

| Sıra | Tek-parça denemesi | Kontrol |
|---:|---|---|
| M01 | TEST01 lens kuponu | Lens açıklığı |
| M02 | CAT06B göz çerçevesi | Kuru geçme ve gerçek kamera görüntüsü |
| M03 | CAT08 kamera taşıyıcı | Kart, lens ve ribbon açıklığı |
| M04 | CAT09 mesafe parçası | Tolerans |
| M05 | CAT05 kulak içi | Beyaz kulakla eşleşme |
| M06 | CAT03 arka kapak | Kasayla kuru montaj |

Önceden basılan parçalar tekrarlanmaz. İlk parça uyumu doğrulanınca kalan adetlere geçilir. Beyaz yüz, kulaklar ve burun sonraki aşamadır. [v0.4 genel uyum listesi](custom/print-fit-v0.4/README.md) ve boş LiPo tepsisi ayrı korunur.

> **Baskı sınırı:** CAT10 kızak, BAT01 ve eski 18650 parçaları baskı dışıdır. Tüm STL klasörünü otomatik kuyruğa vermeyin. v0.5 profil adayı gerçek dilimleme ve yazıcı kontrolünden geçmedi; doğrulanmış G-code/3MF yoktur.

## İlk hareket için dört adım

1. **Besleme ve kontrol kartı:** Mega bağlantısını doğrula; çıkışları yüksüz ölç; sigorta, ana kesme ve düşük hücre gerilimi izleme/korumasını tamamla.
2. **Tek servo:** horn/yük olmadan merkezden küçük adımlarla yön ve güvenli sınırları kaydet.
3. **Tek bacak:** üç servoyla mekanik açıklık, akım, gerilim düşümü ve sıcaklığı ölç.
4. **Destekli gövde:** yeterliliği doğrulanmış kaynakla kademeli olarak 12 servoya geç; sonra yavaş yürüyüş.

XL4016'lar 5 V elektronik ve 6 V masaüstü test hattına adaydır; **12–16 servonun tamamına yeterlilikleri onaylanmadı.** Kart çıkışları paralellenmez. 3S LiPo servolara doğrudan bağlanmaz; ikinci LiPo yalnız robot kapalıyken yedek olarak değiştirilir.

[Bağlantı şablonu](docs/BAGLANTI.md) · [Güç ve test planı](hardware/PCB_PLAN_REV_A.md) · [Uygulama kılavuzu](docs/KILAVUZ.md)

## Kontrol, görüş ve hedef davranışlar

<img src="docs/images/robocat-architecture.svg" alt="Yerel hareket ve merkezi görüş mimarisi" width="900">

| Yerel katman | Merkez katmanı | Sonraki hedef |
|---|---|---|
| Mega + PCA9685 ile hareket; IMU ve mesafe sensörleri | Kameralardan görüntü işleme ve görev kararları | Yaklaşık 1 m takip |
| HC-06 ile manuel kontrol uyarlaması | ESP haberleşmesi ve komut akışı | Sabit kafada iki kamera |
| Bağlantı kaybında durma davranışının uygulanması | Durum ve komut sonuçlarının takibi | Kol kamerası ve kartvizit sunma |

[ESP8266 köprü kodu](firmware/esp8266_bridge/esp8266_bridge.ino) **referans iskelettir**: komutların gerçek motor/ses uygulamaları henüz tamamlanmadı. Protokol/kod bulunması, robotun komutları fiziksel olarak gerçekleştirdiği anlamına gelmez.

[Firmware başlangıcı](firmware/README.md) · [Cihaz protokolü](docs/DEVICE_PROTOCOL.md) · [Sistem](docs/SYSTEM.md)

## Parçalar ve tasarım kaynakları

<table>
<tr>
<td width="50%" align="center">
<img src="docs/images/robocat-parts-head.png" alt="RoboCat kafa parça kataloğu" width="420"><br>
<strong>Kafa parçaları</strong>
</td>
<td width="50%" align="center">
<img src="docs/images/robocat-parts-frame.png" alt="Nova-SM3 gövde ve bacak parça kataloğu" width="420"><br>
<strong>Gövde ve bacak seti</strong>
</td>
</tr>
</table>

| Kaynak | İçerik |
|---|---|
| [Kurulum](docs/KURULUM.md) | Teslim, eksik, kabul ve ilk açılış takibi |
| [Envanter](hardware/INVENTORY.md) | Satın alınan parçalar ve kullanım sınırları |
| [Baskı merkezi](docs/PRINTING.md) | Güncel baskı kaynakları ve engelli parçalar |
| [Özel tasarımlar](custom/README.md) | Kafa, göz ve LiPo tepsisi prototipleri |
| [Nova-SM3](Nova-SM3) | Orijinal gövde, bacak ve elektronik referansları |
| [Nova-SM2](Nova-SM2) | Önceki sürüm kaynakları |
| [Yol haritası](docs/ROADMAP.md) | İlk yürüyüşten kamera ve kola kadar kabul ölçütleri |

Kafa CAD kontrolü gerçek lens/kart/ribbon, vidalar veya gövde bağlantısını kapsamaz. LiPo tepsisi boş/dummy uyum prototipidir. Burun hava girişidir; gaz ölçüm sistemi henüz entegre değildir.

<details>
<summary><strong>Hedef konsepti ve yeniden üretme komutları</strong></summary>

![RoboCat hedef konsepti](docs/images/robocat-concept-v0.3.png)

*Hedef konsepttir. Kol ve bacak kaplamalarının tamamı üretilebilir model olarak hazırlanmış değildir.*

- Kafa: `python custom/robocat-v0.3/generate.py` — CadQuery, numpy, matplotlib.
- Güncel CAT06B: `python custom/petg-stage-v0.5/generate_eye.py`.
- Boş LiPo tepsisi: `python custom/print-fit-v0.4/generate_lipo_tray.py`.
- Uyum paketi: `python custom/print-fit-v0.4/build_pack.py`.
- Diyagramlar: `python docs/diagrams/render_diagrams.py`.

Eski v0.3 toplu paket ihracı kullanımdan kaldırıldı. Kaynak dosya kontrolü başarılı baskı veya mekanik test yerine geçmez.

</details>

## Kaynak ve lisans

[Chris Locke / cguweb-com Arduino-Projects](https://github.com/cguweb-com/Arduino-Projects) projesinden forklanmıştır. Orijinal yazar bilgileri ve [MIT lisansı](LICENSE) korunur. Dışarıdan eklenen tasarımların ayrı lisansları geçerlidir; [kaynak haritasına](docs/SOURCES.md) bakın. Upstream kumanda STL'leri otomatik baskı listemiz değildir; kaynak Gerber'leri RoboCat konfigürasyonumuz için onaylı sayılmaz.
