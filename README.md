# RoboCat

Kamera görüşü, merkez sunucu bağlantısı ve kartvizit sunabilen robot koluyla geliştirilen dört ayaklı robot kedi projesi.

## Geliştirme sırası
1. Arduino Mega ile alt gövde, 12 bacak servosu, MPU6050 ve ön ultrasonik sensörlerin kurulumu ve kalibrasyonu.
2. Sabit kafada iki ESP32-CAM; ultrasonik sensörlerin sabit omuz taşıyıcılarına taşınması.
3. Kendi kontrolcüsü ve üçüncü ESP32-CAM ile robot kol; yaylı kartvizit mekanizması.
4. Merkezde görüntü işleme ve kişi takibi; hareket kontrolü ve bağlantı kaybı davranışları yerelde.

## Batarya taslağı
İki çıkarılabilir 3S1P kartuş, toplam 6 adet 18650. Her pakette ayrı BMS ve sigorta; ortak beslemede uygun ters akım engelleme ve takma akımı sınırlama devresi gerekiyor. Tek paketle yürüyüş akım testiyle doğrulanacak. Batarya değişiminde destek üzerinde oturma ve servo gücünü kesme planlanıyor; destek ve elektrik sistemi henüz tamamlanmadı.

## Tasarımlar
İlk mekanik uyum prototipleri şu an [tasarım dalında](https://github.com/zfrkrc/robodog/tree/design/zk-mechanical-v0.1/custom/zk-v0.1). Bunlar gövdeye veya modüllere birebir uyumu doğrulanmış nihai parçalar değildir. Canlı batarya montajına hazır değildir.

## Kaynak ve lisans
Bu depo [Chris Locke / cguweb-com Arduino-Projects](https://github.com/cguweb-com/Arduino-Projects) projesinden forklanmıştır. Nova-SM2 ve Nova-SM3 kaynak klasörleri, yazar bilgileri ve lisans bildirimleri korunur. Bu sürümlerin donanım ve yazılım farkları vardır; kodlar doğrudan birbirinin yerine yüklenmez. MIT lisansı için [LICENSE](LICENSE) dosyasına bakın. Dışarıdan eklenen mekanik tasarımların lisansları ayrıca geçerlidir.

Proje adı **RoboCat**; GitHub depo adı şimdilik **robodog** olarak kalıyor.
