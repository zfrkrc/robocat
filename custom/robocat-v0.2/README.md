# RoboCat v0.2 — tam kaynak baskı arşivi + ek kedi kafası

## Kapsam
Orijinal Nova-SM3 gövde ve bacak STL geometrileri değiştirilmedi. Yeni kafa, gövdeye eklenen bağımsız bir kabuk prototipidir; orijinal kafa kapağını kaldırıp birebir yerine geçen doğrulanmış bir parça değildir. Arkada kablo erişimi, kameralar için 20 mm göz açıklıkları (60 mm merkez aralığı), kulaklar ve pasif hava girişli çıkarılabilir burun vardır. İki kamera ve koku sensörü için nihai PCB tutucuları modül ölçülerinden sonra belirlenecek. BMS/pil, kafa ve kol ağırlıklarıyla denge testi henüz yapılmadı.

## Baskıdan önce
Nova-SM3 mekanik parçalarının gerçek MG996R motorlarla uyumu henüz doğrulanmadı. Tüm seti körlemesine basmayın. Tek servo yuvası ve tek bacak bileşeni ile horn, rulman ve servo ölçülerini karşılaştırın. Başarılıysa gövde/bacaklara ilerleyin. Orijinal STL'ler karmaşık dönüşlerle kaydedilmiş; dilimleyicide her parçayı uygun düz yüzüne yatırın. Dosya sırası baskı yönü veya montaj sırası anlamına gelmez.

## Yeni kafa
- CAT01_fixed_head_shell_x1.stl: 1 adet, 118×121×42 mm, kulaklar dahil.
- CAT02_rear_lid_x1.stl: 1 adet, 118×90×3 mm.
- CAT03_vented_nose_x1.stl: 1 adet, 42×23×12 mm.
- M3 kapak bağlantısı: kabukta 2,6 mm pilot, kapakta 3,4 mm boşluk. Vida boyu montajla belirlenir; pilleri/kabloları delecek vida kullanmayın.
- Kabuk altındaki iki kayış kanalı geçici uyum testi içindir. 12–13 mm kayışla destekli deneyin; gerçek gövde üzerinde kayma, sensör görüşü ve bacak çarpışması doğrulanmadan yürütmeyin. Rijit gövde adaptörü henüz yok.
- Önce burun ve kapak, ardından kabuk basın. Kabuk düz ön yüzü tablaya gelecek şekilde tasarlanmıştır; 5 mm kulaklardan 3 mm ön yüze geçiş ve slotlar için dilimleyicide destek/ilk katman kontrolü yapın. PETG, 0,2 mm katman, 4 duvar, %20–30 dolgu başlangıç önerisidir.
- Kamera lens/ribbon konumları ve yuva bağlantıları henüz fiziksel doğrulanmadı. Lens deliklerine kartı bastırarak sabitlemeyin; eski prototip kamera beşiği de kesin uyumlu değildir.

## Burun ve koku
Burun yalnız pasif hava girişi ve gelecek sensör için boşluk sağlar. Tek başına koku algılamaz. Sensör seçilmedi: VOC/gaz sensörü ortamda değişim ölçebilir; rastgele kokuyu tanımak veya insan/nesneyi kokusuyla takip etmek ayrı sensör dizisi, örnekleme ve eğitim gerektirir. Isıtıcılı MQ tipi sensörler bu plastik buruna doğrudan yerleştirilmeyecek; ısı, güç ve hava akışı tasarımı ayrıca yapılmalı. Pompa, fan ve sensör soketi bu sürümde yok.

## Kaynak / lisans
Orijinal dosyalar: Christopher M. Locke / cguweb-com, Arduino-Projects, Nova-SM3; arşiv içinde kaynak README ve MIT LICENSE korunur. Fork: https://github.com/zfrkrc/robocat . Yeni kafa CadQuery ile bağımsız üretilmiştir; generate_head.py düzenlenebilir kaynak, STEP dosyaları CAD aktarımı içindir. Dışarıdan alınacak kol tasarımının ticari lisansı ayrıca çözülecek.

## Doğrulama
Yeni üç parça geçerli tek bağlı CAD katısıdır; ölçü/hacim validation.json içinde. Fiziksel baskı, optik hizalama, dayanım, koku algılama, robot üstünde montaj veya tam robot montaj simülasyonu yapılmadı. Bu paket baskı kaynak arşividir, doğrulanmış üretim seti değildir.
