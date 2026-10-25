# RoboCat v0.4 — kontrollü uyum baskısı

2026-10-25. Bu sürüm üretim onayı değildir. Önceki tüm-klasör baskı yaklaşımı yerine tek tek uyum işi listelenir. STL veya STEP geometrisinin geçerli olması mekanik uyum veya başarılı baskı garantisi değildir.

## Güncel kararlar
- Tek Tinylab 3S LiPo 2200 mAh 40C kullanılır; paket nominal 108×35×21 mm, XT60. Satıcı verisi fiziksel ölçüm yerine geçmez.
- Hot-swap yok. Pil değişiminde robot kapatılır. İkinci paket yalnız yedektir; doğrudan paralel bağlanmaz.
- CAT10 kızak, eski 18650 kartuşları ve BAT01 eski kartuş kapağı BASILMAYACAK. Bunlar yeni pil/gövde için uyumlu değildir.
- CAT01 yüz ve CAT02 kasa birbirine uygun ana delik dizilimi taşısa da gerçek kamera/robot gövdesi uyumu henüz doğrulanmadı.
- Kol ve sabit omuzların nihai gövde adaptörleri tamamlanmadı; eski prototip sensör braketi tamamlanmış montaj sayılmıyor.

## İş sırası
Her satır ayrı iştir; otomatik çoklu tabla doldurması yok. Daha önce basılan yüz/kasa tekrar otomatik kuyruğa alınmaz. print_manifest.json yalnız önerilen sözleşmedir; mevcut otomasyon bunu okumuyorsa hiçbir baskıyı kendiliğinden durdurmaz veya engellemez. auto_start=false, bütün işler önizleme ve elle başlatma gerektirir.

1. TEST01 lens kuponu x1, ardından kamera taşıyıcısı x1. Lens/kart/ribbon ve vida aralığı denemesi.
2. Kulak x1 ve kulak içi x1. Baskı toleransı denemesi.
3. CAT01 yüz x1 (zaten basıldıysa yeniden basma).
4. CAT02 kasa x1, yan kayış pencerelerinin köprüleri incelenerek (zaten basıldıysa yeniden basma).
5. CAT03 arka kapak x1.
6. BAT_TEST tepsi x1, yalnız boş veya 108×35×21 mm yumuşak dummy ile uyum denemesi. Canlı LiPo'yu sıkıştırarak veya vidalayarak sabitlemeyin. Tepside gövde bağlantısı, yüksek akım kontak, kapak ve titreşim doğrulaması yoktur; yürüyen robotta kullanıma hazır değildir. Kablo için uçta açık geçit, nominal 112×39×23 mm iç alan vardır; iç köşe yuvarlatmaları ve kayışlar kullanılabilir alanı etkiler.

## Yön ve destek
| Parça | Tabladaki yön | Destek kararı |
|---|---|---|
| TEST01, CAT01, CAT03 | Geniş düz yüz, kaynak STL'de Z=0 tabana gelecek | Düz yerleşimde genel destek beklenmez; ilk katman/delik önizlemesi gerekli |
| CAT08 kamera taşıyıcısı | Düz 34×44 yüz tablada | Düz yerleşimde genel destek beklenmez |
| CAT04 kulak / CAT05 içi | Düz arka yüz tablada; CAD minimum Z=0 | Yatay ince katman, cep ve kulak tepesini önizle |
| CAT02 kasa | 118×90 açık çerçeve kenarı tablada, 37 mm yükseklik | Yanlarda 14 mm kayış penceresi tavanı var. Bu iki bölgeye gerekirse yerel/elle destek eklenmeli; köprüleme makine/filamentte doğrulanmadı |
| BAT_TEST tepsi | Kapalı taban tablada, açık hazne yukarı | Dikey duvarlar, üstten açık kablo geçidi; genel destek beklenmez |

'%5 destek' bütün modele uygulanmış ve test edilmiş ayar değildir. Orca profili destek yoğunluğunu desen aralığıyla da ifade eder. Destek temas yüzeyi, aralığı, köprüleme ve destek boyama önizlemede kontrol edilmeden bir yüzde yeterli sayılmaz. Kaynak profilinde destek zaten açıktır. Bu pakette dilimlenmiş veya destekleri doğrulanmış G-code/Orca 3MF yoktur.

## Yazıcı profili açık noktası
Kullanıcının gönderdiği Ender-3 V2 adlı profil 280×260×310 mm alan, Klipper, Direct Drive, 120 mm/s ilk katman, 500 mm/s travel ve 10000 mm/s² varsayılan ivme tanımlar. Makinenin bunlara gerçekten uygun olduğu doğrulanmadı. Filament türü de kesin değil. Bu ayarları üretim için onaylamıyoruz veya sessizce varsayılan Ender ayarıyla değiştirmiyoruz. Tek parça STL'ler mevcut baskı hacmine sığsa da bu durum hareket/ısıtma profilini doğrulamaz.

## Doğrulama kapsamı
Yeni tepsi tek geçerli CAD katısıdır. Mevcut CAT dosyaları bu sürümde değiştirilmedi. Montaj/dayanım/ısıl/elektrik veya dilimleyici testi yapılmadı. JSON dosyasındaki SHA-256 değerleri bu paketleme anındaki STL içeriğini sabitler. Marka/filament/slicer toleransları fiziksel baskıda doğrulanır.
