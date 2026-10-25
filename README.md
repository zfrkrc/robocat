# RoboCat

> **2026-10-25 — güncel baskı listesi:** [v0.4 tek-parça uyum işleri](custom/print-fit-v0.4/README.md) ve [manifest](custom/print-fit-v0.4/print_manifest.json). CAT10 ile eski 18650 kutuları basılmayacak. Önceden basılan CAT01/CAT02 tekrar otomatik kuyruğa alınmaz. Hot-swap iptal: tek 3S LiPo, kapalıyken pil değişimi. Profil/dilimleme ve montaj henüz doğrulanmadı; toplu üretim paketi değildir.

Kamera görüşü, merkez sunucu bağlantısı ve kartvizit sunabilen robot koluyla geliştirilen dört ayaklı robot kedi projesi.

## Hedef görünüm — konsept
![RoboCat konsept; STL montaj renderı değildir](docs/images/robocat-concept-v0.3.png)
Bu AI görseli tasarım hedefidir. Görseldeki kol, bacak kaplamaları ve tüm gövde bağlantıları bitmiş CAD parçaları değildir.

## Güncel mekanik sürüm: v0.3
![Gerçek v0.3 kafa CAD montajı](custom/robocat-v0.3/cad_head_v0.3.png)

[STL ve STEP parçaları](custom/robocat-v0.3/stl) · [Baskı adetleri ve montaj notları](custom/robocat-v0.3/README.md) · [Parametrik kaynak](custom/robocat-v0.3/generate.py) · [Kafa montajı STEP](custom/robocat-v0.3/head_assembly.step)

Beyaz yüz ve kulaklar, koyu kafa kasası ve göz çerçeveleri, turkuaz kulak içleri ve üç hücreli kartuş kapağı konseptle uyumlu ayrı baskı parçalarıdır. İki kamera kafada sabit, üçüncü kamera ileride kolda olacak. Burun hava girişidir; koku sensörü seçilmedi. Önce TEST01 lens ölçü parçası ve tek kamera taşıyıcısıyla uyum denemesi yapılacak.

**Durum: mekanik uyum prototipi.** Yeni CAD parçaları geçerli tek katı olarak kontrol edildi; modeldeki kafa parçaları ve temsili lensler arasında 0,1 mm³ üzerinde hacim çakışması bulunmadı. Gerçek PCB, vida boyu, kablo, lens mesafesi, gövde bağlantısı ve yük dayanımı fiziksel doğrulanmadı. Kayışlı kızak geçici deneme bağlantısıdır. v0.1/v0.2 kafa parçalarının delik düzenlerini v0.3 ile karıştırmayın.

Tam kaynak baskı paketini yeniden üretmek için gerekli Python ortamında önce `python custom/robocat-v0.3/generate.py`, sonra `python custom/robocat-v0.3/package.py` çalıştırılır. Paket orijinal STL'leri değiştirmeden yeni kafa parçaları, aksesuar prototipleri, baskı listesi ve isteğe bağlı kumandayı toplar. Orijinal parça adetleri montajda doğrulanacak başlangıç tahminleridir.

## Geliştirme sırası
1. Arduino Mega ile alt gövde, 12 servo, MPU6050 ve ultrasonik sensörlerin kurulumu ve kalibrasyonu. Nova-SM3 STL'lerinin gerçek MG996R'lerle uyumu önce tek parçada sınanacak.
2. Sabit kedi kafası, iki ESP32-CAM ve sabit omuzlara sensör taşıma.
3. Ayrı kontrolcüyle robot kol, bilekte üçüncü kamera ve yaylı kartvizit mekanizması.
4. Merkezde görüntü işleme ve kişi takibi; hareket ve bağlantı kaybı davranışları yerelde.

## Güncel batarya planı
Tek Tinylab 3S 11.1 V 2200 mAh 40C LiPo (108×35×21 mm, XT60). Hot-swap iptal; robot kapatılarak pil değiştirilir. İkinci paket yalnız yedektir. Eski 18650 kutuları kullanılmaz. Yeni LiPo tepsisi yalnız boş/dummy uyum testidir; gövde bağlantısı ve titreşim doğrulanmadı. Sigorta, 6 V servo regülasyonu, ayrı elektronik beslemesi ve düşük hücre gerilimi koruması hâlâ gerekli; PCB henüz üretime hazır değil.

## Orijinal modeller / kaynak / lisans
[Orijinal Nova-SM3 STL'leri](Nova-SM3/STL%20Files/SM3%20Files) ve [kumanda STL'leri](Nova-SM3/Remote%20Control/STL%20Files) korunmuştur.

Bu depo [Chris Locke / cguweb-com Arduino-Projects](https://github.com/cguweb-com/Arduino-Projects) projesinden forklanmıştır. Nova-SM2 ve Nova-SM3 kaynak klasörleri, yazar bilgileri ve lisans bildirimleri korunur. Bu sürümlerin donanım/yazılım farkları vardır; kodları doğrudan birbirinin yerine yüklenmez. [MIT lisansı](LICENSE); dışarıdan eklenen mekanik tasarımların lisansları ayrıca geçerlidir.
