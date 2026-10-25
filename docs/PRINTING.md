# RoboCat / baskı merkezi

## Tek yetkili öneri listesi
[Güncel v0.4 talimatı](../custom/print-fit-v0.4/README.md) · [Makine okunur manifest](../custom/print-fit-v0.4/print_manifest.json).

Manifest bir önerilen entegrasyon sözleşmesidir. Yazıcı yazılımının bunu gerçekten okuduğu doğrulanmadı; bu dosya tek başına kuyruğu bloke edemez. Klasördeki bütün STL'leri otomatik keşfedip basmak doğru akış değildir. auto_start=false; önizleme ve elle başlatma gerekir.

## Ayrı işler
| Sıra | İş | Adet | Durum |
|---:|---|---:|---|
| 1 | TEST01 lens kuponu | 1 | Uyum denemesi |
| 2 | CAT08 kamera taşıyıcısı | 1 | Kart/lens/ribbon ölçüsü |
| 3 | CAT04 kulak | 1 | Tolerans denemesi |
| 4 | CAT05 kulak içi | 1 | Tolerans denemesi |
| 5 | CAT01 yüz | 1 | Zaten basılıyorsa tekrar sıraya alma |
| 6 | CAT02 kasa | 1 | Zaten basılıyorsa tekrar sıraya alma; iki yan köprüyü incele |
| 7 | CAT03 arka kapak | 1 | Kuru montaj |
| 8 | BAT_TEST LiPo tepsisi | 1 | Boş/dummy deneme; canlı paket montajı değil |

Bu adetler tamamlanmış robotun üretim BOM'u değildir. Örneğin kafa sonunda iki kulak ve iki kamera taşıyıcısı kullanır; ilk tabloda yalnız birer uyum denemesi vardır.

## Basılmayacak parçalar
CAT10 kızak; eski 18650 kartuş gövdesi/kapağı/kızağı; BAT01 eski kartuş kapağı; nihai gövde bağlantısı doğrulanmamış omuz sensör braketi. Bu dosyalar tarihçe için repoda durur, aktif baskı onayı değildir.

## Yön / destek
Geniş düz yüzü tabana yatırılan yüz, kapak, kupon ve taşıyıcıda genel destek beklenmez; yön gerçekten bu olmalıdır. CAT02 açık çerçeve dik duvarlarla basılır, yanlarda 14 mm pencere tavanları için yerel destek/köprüleme incelenir. '%5 destek' tek başına doğrulanmış reçete değildir. Gönderilen Orca profilinde destek açıktı; uygulanmış son dilimleme ve baskı yerleşimi repoda yoktur.

## Makine profili
Gönderilen Ender-3 V2 adlı profil Klipper, Direct Drive, 280×260×310 mm alan ve yüksek hız/ivme tanımlar. Gerçek donanımın bu ayarlara uygunluğu, filament ve son G-code doğrulanmadı. Bu saptama yazıcının kesin stok Ender olduğu anlamına gelmez; ayarlar sessizce değiştirilmedi.

## Paket üretme
1. Gerekirse `python custom/print-fit-v0.4/generate_lipo_tray.py`.
2. `python custom/print-fit-v0.4/build_pack.py`.

Yeni ZIP yalnız kontrollü uyum işlerini toplar, eski tüm-parça paketi değildir. v0.3 `package.py` eski ihracı durdurur. v0.1/v0.2/v0.3 ZIP'leri otomatik üretim girdisi olarak kullanmayın. Paketleyici SHA-256 içerik kontrolleri yapar; dilimleme, baskı, mekanik montaj veya güvenlik testi yapmaz.
