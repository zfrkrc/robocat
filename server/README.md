# RoboCat sunucu servisi (v0.1)

Kamera görüntüsü alımı, görüntü işleme sonuçları, telemetri ve **komut kuyruğu** için küçük FastAPI servisi. Robotun servo döngüsü **yerelde** çalışır; bu servis yalnızca hedef/izleme/komut katmanıdır.

## Hızlı başlangıç

```bash
cd server
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
# panel: http://127.0.0.1:8080/   ·  API: /docs
```

Docker:

```bash
docker build -t robocat-server server
docker run -p 8080:8080 -v $PWD/data:/data -e ROBO_DATA_DIR=/data robocat-server
```

Testler: `cd server && python3 -m pytest -q` (9 test; ağ/model gerekmez).

## Uçlar

| Metot | Yol | Kim kullanır |
|---|---|---|
| POST | `/api/v1/cameras` | kurulum: kamera kaydı |
| POST | `/api/v1/cameras/{id}/frame` | ESP32-CAM / köprü (JPEG gövde) |
| GET | `/api/v1/cameras/{id}/stream.mjpg` | tarayıcı paneli |
| GET | `/api/v1/cameras/{id}/detections` | panel / merkez |
| POST | `/api/v1/robots/{id}/telemetry` | robot köprüsü |
| GET | `/api/v1/robots/{id}/state` | panel |
| POST | `/api/v1/robots/{id}/commands` | operatör / merkez |
| GET | `/api/v1/robots/{id}/commands/next` | robot köprüsü (poll) |
| POST | `/api/v1/robots/{id}/commands/{cid}/ack` | robot köprüsü |
| POST | `/api/v1/robots/{id}/emergency_stop` | operatör |

Tam sözleşme: [`docs/SERVER_API.md`](../docs/SERVER_API.md) · davranış: [`docs/MISSION.md`](../docs/MISSION.md).

Panelde görev kartı (takip / isimle durdur / çevre kontrolü / evet-hayır / sensör) ve **web'den kare yükleme** vardır.

## Ortam değişkenleri

| Değişken | Varsayılan | Not |
|---|---|---|
| `ROBO_DATA_DIR` | `./data` | SQLite + kareler |
| `ROBO_DETECTOR` | `motion` | `motion` · `yolo` · `none` |
| `ROBO_YOLO_ONNX` | — | `yolo` seçilirse model yolu |
| `ROBO_ARUCO` | `1` | ArUco işaretçi tespiti |
| `ROBO_FRAME_RETENTION` | `200` | kamera başına saklanan kare |
| `ROBO_COMMAND_TTL_S` | `30` | claim süresi; sonra `expired` |
| `ROBO_CORS_ORIGINS` | `*` | paneli ayrı origin'den açacaksan kısıtla |

## Kapsam ve dürüst sınırlar

- **`motion`** = MOG2 arka plan çıkarma. "İnsan tanıma" değil, **hareketli bölge** verir.
- **`yolo`** = `ROBO_YOLO_ONNX` verilirse yalnız sınıf 0 (person) kutuları. Model olmadan test edilmedi.
- **ArUco** gerçek ölçülebilir hedeftir; kalibrasyon ve konum için bunu tercih et.
- **Kimlik doğrulama yok (v0.1)**: LAN dışına açma; ters vekil + token sonraki adım.
- Video kaydı yok; kareler JPEG olarak döngüsel saklanır (varsayılan 200).
- **Cihaz köprüsü (ESP8266):** `POST /api/v1/device/{id}/sync` + `X-Device-Key` (`ROBO_DEVICE_KEYS`). Ayrıntı: [`docs/DEVICE_PROTOCOL.md`](../docs/DEVICE_PROTOCOL.md), örnek: `firmware/esp8266_bridge/`.
- E-stop **sunucu tarafı kapıdır**; gerçek güvenlik **robot üzerindeki yerel stop**tur. İkisi birlikte kullanılmalı.
