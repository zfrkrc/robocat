# RoboCat v0.5 — önce metalik PETG

DURUM: baskı öncesi hazırlık. Kullanıcı PETG geldikten sonra açıkça “bas” diyecek. Şu anda baskı başlatılmadı; G-code gönderilmedi. `metallic_queue.json` önerilen iş sözleşmesidir, mevcut yazıcı yazılımına entegrasyonu doğrulanmadı.

## İlk sıra: METALİK
1. M01: TEST01 kupon, bir adet (zaten basıldıysa atla).
2. M02: düzeltilmiş CAT06B, **önce bir adet**. 20 mm yüz deliğinde kuru yerleşim, gerçek kamera ile canlı görüntü ve kenar kararması kontrolü. Yapıştırma yapılmayacak.
3. M03: tek kamera taşıyıcısı (zaten basıldıysa atla).
4. M04: tek mesafe parçası, tolerans kontrolü.
5. M05: tek kulak içi. Beyaz kulakla eşleşme denemesi yapılmadan seri basma.
6. M06: arka kapak, kasa ile kuru montaj (önceden basıldıysa atla).

Bunlar bağımsız işlerdir; tümünü bir tabla/kuyrukta otomatik başlatma. İlk kupon/çerçeve başarısızsa sonraki işe ilerleme. İkinci göz ve kalan adetler ilk uyumdan sonra ayrıca onaylanır.

Metalik PETG'nin aşındırıcı veya özel nozul gerektirdiği ismine bakılarak varsayılmaz; gerçek ürün etiketi ve teknik bilgi kontrol edilecek. Beyaz aşama yüz, kulaklar ve burundur; şimdilik bu sıraya dahil edilmez. Kasa zaten basılıyor bildirildiği için tekrar sıraya eklenmedi.

## CAT06B düzeltmesi
- Eski STL üç ayrı, birbirine 0,05 mm örtüşen kapalı kabuktan oluşuyordu.
- Yeni `generate_eye.py` Boolean union ile **tek geçerli CAD katısı** üretir.
- Dış çap 28 mm; toplam yükseklik 4,5 mm; 19,6×1,5 mm merkezleme bileziği; 7×7 mm geçiş; 9×9×1 mm ön cep.
- STL büyük ön yüzü tabana gelecek, bilezik yukarı bakacak şekilde normalize edildi; min Z=0. Bilezik aşağı basılıp 4,2 mm dış çıkıntı oluşturulmamalı.
- Mevcut CAT01 ile yerleştirilmiş iki çerçevenin basılı geometri kesişimi kontrol edildi. Kamera, yapıştırıcı, lens derinliği/görüş alanı, titreşim ve ısı kapsam dışı.
- 7×7 açıklığın optiği kesmediği görülmeden yapıştırma yok. Lens çevresinde yapıştırıcı kullanımı/kimyasal uygunluğu ayrıca değerlendirilecek.
- Eski yol `custom/robocat-v0.3/stl/CAT06B_eye_bezel_7x7_boss_x2.stl` de aynı düzeltilmiş içerikle güncellenir. Eski indirilmiş dosyaların hash'i farklıdır; manifestteki güncel SHA-256 esas alınır.

## Dilimleme adayı
`Orca_RoboCat_PETG_Fit_Candidate.json`, kullanıcının gönderdiği process presetinin kopyasından hazırlanmış bir **işlem profili adayıdır**. Yazıcı/filament profilini veya firmware'i değiştirmez. PETG sıcaklığı içermez; gerçek makara etiketi görülmeden nozzle/tabla sıcaklığı atanmaz.

Önerilen başlangıç: 0,20 mm katman, 4 duvar, %25 gyroid; ilk katman 20, dış duvar 30, iç duvar 45, travel 100 mm/s; normal ivme 500 mm/s². Genel destek ve prime tower kapalı; bu yalnız listedeki düz yönlü uyum parçaları içindir. CAT02 kasa için ayrıca destek/köprü incelemesi gerektiğinden bu sırada yoktur. Profil içeriği gerçek OrcaSlicer'da açılıp dilimlenmedi; uyumluluk/çıktı doğrulanmadı.

Kuşkulu Ender-3 V2 yazıcı profilindeki 280×260×310 alan, Klipper/Direct Drive ve makine limitleri doğrulanmadan bu process profili tek başına baskıyı onaylamaz. Filament çapı 1,75 mm/nozul 0,4 mm bilgileri de fiziksel doğrulanacak.

## Bas komutundan önce
- Metalik makara takılı; ürün/etiket sıcaklık aralığı belli.
- Doğru gerçek yazıcı ve mevcut çalışma profili seçili.
- Job SHA-256, yön, ölçek mm, adet ve tabla önizlemesi kontrol edildi.
- G-code sıcaklık/hareket/başlangıç komutları incelendi; ilk katman gözetimi sağlandı.
- Kullanıcının açık başlatma komutu alındı. Bu belge veya JSON kendi başına böyle bir izin sayılmaz.

Eski CAT10, BAT01 ve 18650 parçaları engelli kalır. Gövde, servo uyumu, kol ve PCB bu göz hazırlığıyla tamamlanmış olmaz.
