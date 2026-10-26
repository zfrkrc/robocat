# RoboCat sunucu API sözleşmesi — v1

Yerel ajan (robot köprüsü / ESP32-CAM) ile sunucu arasındaki **tek sözleşme**. Sürüm `v1`; uçlar `/api/v1` altındadır. Sözleşme değişirse sürüm artırılır.

Sunucu bir **hareket denetleyicisi değildir**: servo döngüsü yerelde çalışır, sunucu hedef/komut üretir. Ağ koptuğunda robot son komutu uygulayıp **güvenli durmalıdır**.

## 1) Kimlikler

| Alan | Kural | Örnek |
|---|---|---|
| `camera_id` | `^[a-z0-9][a-z0-9_-]{1,31}$` | `head-left`, `arm-cam` |
| `robot_id` | aynı | `robocat-1` |
| `role` | `head_left` · `head_right` · `arm` · `other` | `head_left` |

Kamera önce `POST /api/v1/cameras` ile kaydedilir; kayıtsız kameradan kare **404** döner.

## 2) Kamera → sunucu (görüntü)

```
POST /api/v1/cameras/{camera_id}/frame
Content-Type: image/jpeg
<ikili JPEG gövde>
```

| Durum | Anlam |
|---|---|
| `202` | kabul edildi (kuyruğa alındı) |
| `400` | boş gövde |
| `404` | kamera kayıtlı değil |
| `413` | gövde `ROBO_MAX_FRAME_BYTES` (varsayılan 4 MB) üstü |
| `415` | JPEG değil (SOI `FF D8` yok) |

Yanıt:

```json
{"camera_id":"head-left","frame_id":12,"seq":12,"ts":1761480000.12,"bytes":23114,"queued":true,"analysis":null}
```

- `?sync=1` → analiz aynı istekte yapılır, `analysis` dolu döner (test/düşük fps için).
- Önerilen gönderim: **2–5 fps**, 320×240 veya 640×480, JPEG kalite 70–85. 3 kamera × 5 fps = 15 kare/s; kuyruk 256, taşarsa kare yine saklanır, `queued=false`.
- Sunucu saati (`ts`) kayıt için geçerlidir; robot saati kullanılmaz.

Sunucudan okuma:

```
GET /api/v1/cameras/{camera_id}/latest.jpg     -> son kare (image/jpeg)
GET /api/v1/cameras/{camera_id}/stream.mjpg    -> MJPEG akış (panel)
GET /api/v1/cameras/{camera_id}/detections?limit=50&since=<unix>
```

## 3) Tespit çıktısı

```json
{"id":41,"frame_id":12,"camera_id":"head-left","ts":1761480000.9,
 "kind":"motion","label":"moving_region","score":0.62,
 "x":40,"y":18,"w":85,"h":120,"extra":{"area_px":10200}}
```

| `kind` | Anlam | Güvenilirlik |
|---|---|---|
| `motion` | MOG2 hareketli bölge | “insan” değil; hareket |
| `person` | YOLO sınıf 0 | model varsa; sürüm doğrulanmadı |
| `aruco` | ArUco işaretçi | ölçülebilir, kalibrasyon için tercih edilir |

`x,y,w,h` piksel koordinatıdır (sol üst + genişlik/yükseklik). `extra.marker_id` ArUco kimliğidir.

## 4) Robot → sunucu (telemetri)

```
POST /api/v1/robots/{robot_id}/telemetry
{"battery_v":11.6,"current_a":2.8,"imu":{"pitch":1.2,"roll":-0.4},"extra":{"joints":[512,300,410]}}
```

`201` döner. Saklama: robot başına son `ROBO_TELEMETRY_RETENTION` (5000) kayıt. `GET /api/v1/robots/{id}/state` → `{estopped, telemetry, commands[10]}`.

## 5) Komut kuyruğu (at-least-once)

```
POST /api/v1/robots/{robot_id}/commands        {"kind":"move","params":{"linear":0.1}}
GET  /api/v1/robots/{robot_id}/commands/next   -> komut | null
POST /api/v1/robots/{robot_id}/commands/{id}/ack {"ok":true,"note":"tamam"}
```

| `kind` | `params` örneği | Not |
|---|---|---|
| `move` | `{"linear":0.1,"strafe":0,"rotate":0}` | -1..1 normalize |
| `look` | `{"pan":10,"tilt":-5}` | derece |
| `greet` | `{}` | kartvizit/selam senaryosu |
| `idle` | `{}` | pozisyonda bekle |
| `calibrate` | `{}` | yerel kalibrasyon modu |
| `stop` | `{}` | **e-stop açıkken tek kabul edilen** |

Yaşam döngüsü: `queued → claimed → done|failed` (+ `expired`).

- `next` çağrısı komutu **atomik** olarak `claimed` yapar ve `claimed_at` yazar.
- `ROBO_COMMAND_TTL_S` (30 s) içinde `ack` gelmezse komut `expired` olur ve yeniden dağıtılmaz.
- Ağ tekrarı olabileceği için robot **aynı `id`'yi iki kez uygulamamalı** (son işlenen id'yi sakla).
- Komut geçerlilik süresi dolduysa robot **uygulamamalı**, `ack` yerine yeni `next` almalı.

## 6) Acil durdurma

```
POST /api/v1/robots/{robot_id}/emergency_stop  {"engaged":true,"note":"operatör"}
```

- `engaged=true` iken `move/look/greet/idle/calibrate` → **409**; yalnız `stop` kabul edilir.
- `engaged=false` ile açılır. Her iki geçiş `events` tablosuna yazılır.
- **Bu sunucu tarafı bir kapıdır.** Gerçek güvenlik: robot üzerindeki yerel stop + güç kesme. Sunucu kapalıyken robot hareket etmemeli.

## 6b) Görev (mission) uçları

```
POST /api/v1/robots/{id}/mission/start            -> {"state":"follow"}
POST /api/v1/robots/{id}/mission/stop             -> {"state":"idle"}
GET  /api/v1/robots/{id}/mission                  -> {"state":..., "context":{...}}
POST /api/v1/robots/{id}/mission/event            {"type":"name_called"|"env_check"|"scan_result"|"person_seen"|"answer"|"sensor"|"resume"|"operator_stop","data":{}}
GET  /api/v1/robots/{id}/recognize?camera_id=..   -> deterministik karar
POST /api/v1/robots/{id}/mission/scan?camera_id=..-> karar + göreve işleme
```

Davranış sözleşmesi: [MISSION.md](MISSION.md). `answer` olayı `{"yes":true|false}`; `sensor` olayı `{"alcohol_ppm":..}` veya `{"alcohol_mv":..}` taşır.

## 7) Sağlık ve hata biçimi

```
GET /api/v1/health
{"ok":true,"version":"0.1.0","detector":{"detector":"motion","queued":0,"processed":42,"failed":0},"cameras":3}
```

Hatalar FastAPI standardı: `{"detail":"..."}` + uygun HTTP kodu. İstemci `4xx`'i kalıcı, `5xx`'i geçici saymalı ve üstel geri çekilmeli.

## 8) Bilinen sınırlar (v1)

- Kimlik doğrulama yok → **yalnız LAN**; dışa açılacaksa ters vekil + token şart.
- Video kaydı yok; JPEG halka tamponu (`ROBO_FRAME_RETENTION`).
- `motion` insan sınıflandırması değildir; `person` için ONNX model gerekir ve model doğrulanmamıştır.
- Çoklu sunucu / yatay ölçek yok (tek SQLite).
