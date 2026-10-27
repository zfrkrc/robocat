# Kaynak haritası ve lisans

RoboCat, Chris Locke / cguweb-com [Arduino-Projects](https://github.com/cguweb-com/Arduino-Projects) deposundan forklanmıştır. Kaynak yazar bilgileri ve [MIT LICENSE](../LICENSE) korunur.

| Dizin | Rol |
|---|---|
| `custom/petg-stage-v0.5` | Önce metalik PETG için güncel ilk uyum aşaması |
| `custom/print-fit-v0.4` | Genel uyum işleri ve LiPo boş tepsi prototipi |
| `custom/robocat-v0.3` | Kafa CAD/STL/STEP kaynakları; CAT10 ve eski pil kapağı aktif baskıda engelli |
| `custom/zk-v0.1` | Eski mekanik prototipler; güncel montaj olarak kullanılmaz |
| `hardware` | Satın alınan envanter, güç/test planı ve pin önerisi |
| `docs` | Güncel proje dokümanları ve görseller |
| [`Nova-SM2`](../archive/upstream/Nova-SM2) | Orijinal Nova SM2 kaynakları; farklı servo/PCA düzeni içerebilir |
| `Nova-SM3` | Orijinal Nova SM3 mekanik, elektronik ve yazılım; RoboCat'in onaylı üretim seti değildir |
| `Nova-SM3/Remote Control` | El kumandası; robot gövdesi değil, opsiyonel |
| [`BlackWidow-Hexapod`](../archive/upstream/BlackWidow-Hexapod) | Upstream altı ayaklı proje; RoboCat'e dahil değil |
| [`RobotArm-6DOF`](../archive/upstream/RobotArm-6DOF) | Upstream kol kaynakları; bizim dört servo kolumuza doğrulanmış aktarım değil |
| [`Pot_ProtoBox`](../archive/upstream/Pot_ProtoBox), [`Spectrum-Analyzer`](../archive/upstream/Spectrum-Analyzer) | Upstream diğer projeler; RoboCat baskı listesine dahil değil |

Nova-SM2 ve RoboCat dışındaki diğer dört upstream proje [arşiv merkezine](../archive/README.md) taşındı. İçerikleri ve kendi iç dizin yapıları korundu; güncel RoboCat belgelerinin bağlantıları yeni yollara uyarlandı. Nova-SM3 referans yolları yerinde bırakıldı. Bu depodaki bir dosyanın varlığı otomatik baskı veya PCB sipariş onayı değildir.

Yeni RoboCat parametrik parçaları kendi CadQuery kaynaklarıyla sağlanır. Dışarıdan alınan Thingiverse/CAD/kol dosyaları ayrı lisans şartları taşıyabilir. Özellikle EEZYbotARM için ticari izin doğrulanmadan satış sürümüne alınmayacak. MIT yazılım lisansı bütün üçüncü taraf mekanik tasarımları otomatik yeniden lisanslamaz.
