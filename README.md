# RoboCat

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

## Batarya taslağı
İki çıkarılabilir 3S1P kartuş, toplam 6 adet 18650. Her pakette ayrı BMS ve sigorta; ortak beslemede ters akım engelleme ve takma akımı sınırlama devresi gerekiyor. Tek paketle yürüyüş akım testiyle doğrulanacak. Batarya değişiminde destek üzerinde oturma ve servo gücünü kesme planlanıyor; destek ve elektrik sistemi henüz tamamlanmadı. Batarya kutuları canlı hücre montajına hazır değildir.

## Orijinal modeller / kaynak / lisans
[Orijinal Nova-SM3 STL'leri](Nova-SM3/STL%20Files/SM3%20Files) ve [kumanda STL'leri](Nova-SM3/Remote%20Control/STL%20Files) korunmuştur.

Bu depo [Chris Locke / cguweb-com Arduino-Projects](https://github.com/cguweb-com/Arduino-Projects) projesinden forklanmıştır. Nova-SM2 ve Nova-SM3 kaynak klasörleri, yazar bilgileri ve lisans bildirimleri korunur. Bu sürümlerin donanım/yazılım farkları vardır; kodları doğrudan birbirinin yerine yüklenmez. [MIT lisansı](LICENSE); dışarıdan eklenen mekanik tasarımların lisansları ayrıca geçerlidir.
