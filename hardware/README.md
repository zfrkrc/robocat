# RoboCat donanım merkezi

- [Satın alınan parçalar](INVENTORY.md): toplam 16 MG996R, 3 ESP32-CAM, 5 HC-SR04, 2 MPU6050.
- [Proje/donanım fotoğrafları](../docs/BUILD_PHOTOS_2026-10-26.md): 20 kare; HW-373 güç modülü ve süpürge parçaları BOM dışı.
- [Güncel güç/test planı](PCB_PLAN_REV_A.md): içerik rev B; tek 3S LiPo ve hot-swap yok.
- [Pin önerisi](PINMAP_REV_A.csv): fiziksel arayüz/pull-up/lojik seviye kontrolleri bekliyor.
- [Kontrol mimarisi](../docs/images/robocat-architecture.svg).
- [Güç mimarisi](../docs/images/robocat-power.svg).

PCB durumu: bağlantı planı. Şematik, yerleşim, ERC/DRC veya RoboCat için doğrulanmış Gerber yoktur. Nova kaynak dizinindeki Gerber arşivi farklı orijinal donanım içindir; doğrudan RoboCat siparişine gönderilmeyecek.

Önce modüllerle masaüstü test. Motor gücü breadboard/sinyal jumperı üzerinden geçirilmez. Satın alınacak regülatör, sigorta ve koruma parçaları test akımı ve gerçek modül verilerine göre seçilecek.
