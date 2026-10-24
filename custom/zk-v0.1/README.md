# Robodog ZK v0.1 — mekanik uyum prototipi

2026-10-24. Birimler mm. Bu klasördeki yeni parçalar bağımsız parametrik CadQuery geometrisidir; Nova STL'lerinin değiştirilmiş sürümleri değildir. Repo kökündeki MIT lisansı geçerlidir; kaynak Nova dosyaları ve telif bildirimleri korunur.

## Kararlar
- Sabit kafa; gözlerde 2 ESP32-CAM, kolda üçüncü kamera.
- İki HC-SR04, hareketli bacak/servo yerine sabit gövdenin omuz yakınındaki taşıyıcılarına yerleştirilecek.
- 2 bağımsız, sökülebilir 3S1P kartuş; toplam 6 adet 18650.
- Kol ve kafa hareket mekanizması bu sürüme dahil değildir.

## Baskı listesi
| STL | Adet | Açıklama |
|---|---:|---|
| 01_fixed_face_x1 | 1 | 120×60×3 yüz; 64 mm kamera merkezi aralığı, 20 mm göz açıklıkları |
| 02_camera_cradle_x3 | 3 | 29×42 mm nominal kart boşluğu; kablo bağıyla tutma, karta özel vida düzeni değil |
| 03_shoulder_ultrasonic_x2 | 2 | 17 mm transdüser açıklıkları, 26 mm merkez aralığı; modül fotoğrafıyla doğrulanacak |
| 04_3s_cassette_body_x2 | 2 | 112×70×27; 70 mm hücre boyu boşluğu, ayrı elektronik bölmesi |
| 05_3s_cassette_lid_x2 | 2 | M3 bağlantılı kapak; 2,6 mm pilot delikler gerektiğinde işlenecek |
| 06_strap_dock_x2 | 2 | Kartuştan bağımsız gövde kızağı; kayışla tutma, otomatik kilit yok |
| 07_face_angle_adapter_x2 | 2 | Genel ayar braketleri; gövdeyle birebir delik uyumu henüz yok |

STL baskı içindir. Aynı klasörde STEP dosyaları ve üst klasörde düzenlenebilir generate.py vardır.

## Gerçekte doğrulanmış olanlar
CadQuery katıları geçerli ve her parça tek bağlı katı olarak kontrol edildi. Boyutlar validation.json içinde. preview.png gerçek CAD geometrilerinden üretildi. Fiziksel baskı/uyum, yük, darbe ve termal test yapılmadı.

## Önce boş uyum baskısı
İlk olarak tek kamera yuvası, tek sensör yuvası, tek kartuş ve kızağı basın. Öneri: PETG, 0,2 mm katman, 4 duvar, %25–35 dolgu; yüzler/tabanlar XY düzleminde. Sensör braketinin yatay çıkıntıları için dilimleyicide destek ihtiyacını kontrol edin. Bu ayarlar mekanik test yerine geçmez.

Kamera ve sensör yuvaları delik/boşluk ölçüleri varsayımsaldır. Gerçek kartı ölçmeden zorlayarak takmayın. Yüz ve kamera yuvası bağımsız parçalar olarak verilmiştir; nihai optik hizalama, lens/ribbon boşluğu ve bağlantı elemanı dizilimi doğrulanmamıştır. Mevcut gövdeye birebir oturduğu iddia edilmez. Gövde taşıyıcı ölçüleri ve delik koordinatları alınınca montaj adaptörü revize edilecek. Kol kamerası yuvasının kol bağlantısı ayrıca tasarlanacak.

## Batarya sınırları
Bunlar yalnızca mekanik maket muhafazalardır: kutup kontakları, konektör kesiti ve anahtarlaması, BMS montajı, izolasyon geometrisi, hücre sabitleme/pedleri ve gerçek hot-swap devresi henüz tasarlanmamıştır. Hücre yuvalarında metal vida/kontak kullanmayın; ilk denemeyi enerjisiz/dummy hücrelerle yapın. Elektrik tasarımı tamamlanmadan canlı paket monte etmeyin. Yaylı genel pil yatağı üzerinden servo yüksek akımı taşınmayacak.

Her kartuş için bağımsız 3S BMS/sigorta ve güç yolunda ters akım engelleme + ilk takma akımı sınırlaması gerekiyor. Gerilim izlemesi kartuş başına yapılmalı; yüzde yalnız gerilimden kesin bulunamaz. Tek kartuş yürüyüşü yüksek deşarj hücresi, BMS ve yolun tam akım testine bağlıdır. Servolar/elektronik doğrudan 3S çıkışa bağlanmayacak. 3S Li-ion için uygun 12,6 V CC/CV şarj kullanılacak. Gövde desteği/oturma ayakları bu pakette yoktur; pil değiştirmede servo gücünü kesmeden önce destek tasarlanıp test edilmelidir.

## İhtiyaç duyulan ölçüler
1. Gerçek basılan gövde: KDY orijinal mi Nova SM2 mi? Ön montaj delikleri ve iç hacim.
2. ESP32-CAM PCB, lens ve kablo ölçüleri; ön/arka fotoğraf.
3. HC-SR04 ve sabit omuz taşıyıcısının ölçüleri; bacak süpürme hacmi.
4. Hücre marka/model, boy/çap; BMS boyutu; yüksek akım konektörü ve kablo çapı.
5. Baskı yazıcısı, nozul ve malzeme.

## Yeniden üretim
`python generate.py` (cadquery, numpy, matplotlib). validation.json ve stl/ içindeki STL/STEP dosyalarını üretir.
