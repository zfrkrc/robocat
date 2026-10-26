# RoboCat cihaz protokolü — ESP8266 / köprü (v1)

Sahadaki cihaz (ESP8266, pentest ajanı, köprü) **tek HTTP turunda** durum bildirir ve komut alır. Sunucu tarafı: `server/app/main.py` → `/api/v1/device/{device_id}/sync`.

## 0) DNS durumu (2026-10-26)

| Ad | Sonuç |
|---|---|
| `zk.net.tr` | Cloudflare (`rick/vita.ns.cloudflare.com`) → 104.21.36.99 / 172.67.192.79 |
| `esp32.zk.net.tr` | **NXDOMAIN** (kayıt yok) |

Cihaz için bir adres gerekli. Üç seçenek:

1. **LAN (önerilen):** cihaza sabit IP/DHCP rezervasyonu; sunucuya LAN IP ile bağlan (`http://172.16.16.x:8080`).
2. **İç DNS:** yerel DNS'e `esp32.zk.net.tr → 172.16.16.x` kaydı (dışarı sızmaz).
3. **Dış erişim gerekiyorsa:** Cloudflare **proxy'li A** kaydı + **Cloudflare Tunnel** (origin'e giden port yok). Doğrudan A kaydı ile 8080 açmak **önerilmez**.

## 1) Kimlik ve yetki

- Cihaz kimliği: `[a-z0-9][a-z0-9_-]{1,31}` (örn. `robocat-1`).
- Sunucuda anahtar: `ROBO_DEVICE_KEYS="robocat-1:<rastgele>"` (virgülle çoklu).
- İstek başlığı: `X-Device-Key: <rastgele>`.
- Anahtar tanımlı değilse **yalnız loopback** kabul edilir (geliştirme). Üretimde mutlaka tanımla.
- Cihaz→robot eşlemesi: `ROBO_DEVICE_ROBOTS="robocat-1:robocat-1"` (tanımsızsa aynı ad).

## 2) Tek tur

```
POST /api/v1/device/{device_id}/sync
Content-Type: application/json
X-Device-Key: <key>
```

İstek (≤ ~1 KB önerilir):

```json
{"ts":1761480000,"rssi":-62,"battery_v":11.7,"firmware":"esp8266-bridge-0.1",
 "sensors":{"current_a":1.8,"pitch":0.4},
 "events":[{"type":"name_called"}],
 "ack":[{"id":41,"ok":true}]}
```

Yanıt:

```json
{"server_time":1761480002.1,"robot_id":"robocat-1","next_poll_s":2,
 "commands":[{"id":42,"kind":"say","params":{"text":"Merhaba"}}],
 "config":{"env_check_s":60,"answer_timeout_s":8,"sensor_timeout_s":20,"command_ttl_s":30},
 "events_applied":1,"acks_applied":1}
```

| Durum | Anlam | Cihaz davranışı |
|---|---|---|
| `200` | tur başarılı | `next_poll_s` kadar bekle |
| `401` | anahtar hatalı | 10 s bekle, anahtarı kontrol et (logla) |
| `429` | çok sık | geri çekilmeyi iki katına çıkar (≤15 s) |
| `503` | anahtar yapılandırılmamış | kurulum hatası; 30 s bekle |
| `5xx` | sunucu hatası | üstel geri çekilme |

- Aynı turda **en fazla 2 komut** döner; cihaz tamponu küçük tutulur.
- `events` ve `ack` en fazla 8'er öğe.
- Gövde sınırı: `ROBO_MAX_FRAME_BYTES` (kare uçları için); sync gövdesi için 16 KB pratik sınır.
- Hız sınırı: cihaz başına `ROBO_DEVICE_MIN_INTERVAL_S` (varsayılan 0,4 s).

## 3) Komut yaşam döngüsü

`queued → claimed (sync ile) → done|failed (ack)`; `ROBO_COMMAND_TTL_S` (30 s) içinde ack gelmezse `expired`.

- **At-least-once:** ağ tekrarı olabilir. Cihaz son uyguladığı `id`'yi saklamalı, aynı id'yi **iki kez uygulamamalı**.
- Ack bir sonraki turda gönderilebilir; bu arada TTL dolabilir — bu normaldir, komut yeniden dağıtılmaz.
- `stop` her zaman en yüksek öncelik; e-stop açıkken **yalnız** `stop` üretilir.

## 4) Olaylar (cihaz → sunucu)

| `type` | `data` | Etki |
|---|---|---|
| `name_called` | — | robot durur, "Efendim?" (görev `hold`) |
| `env_check` | — | ortam taraması başlatır |
| `scan_result` | `{"accepted":true,"label":"marker_7"}` | taramayı kapatır |
| `person_seen` | `{"source":"pir"}` | tanışma akışını başlatır |
| `answer` | `{"yes":true|false}` | alkol testi sorusunun cevabı |
| `sensor` | `{"alcohol_ppm":120}` veya `{"alcohol_mv":1800}` | ölçüm sonucu |
| `resume` | — | beklemeden takibe döner |
| `operator_stop` | — | görevi bitirir |

Davranış ayrıntısı: [MISSION.md](MISSION.md).

## 5) Güvenlik notları

- Cihaz anahtarı **cihaz başına** ayrı; sızarsa yalnız o cihazı döndür (`ROBO_DEVICE_KEYS` güncelle).
- LAN içinde HTTP kabul edilebilir; dış ağa çıkacaksa **HTTPS** (ters vekil / Cloudflare Tunnel) kullan. ESP8266'da TLS yavaştır; tercihen LAN.
- Sunucu saati kayıt için geçerlidir; cihaz saati güvenilmez.
- Cihaz **yerel stop**'tan sorumludur. Sunucu kapalı/ağ koptuğunda hareket etmemeli.
- `stop` komutu ACK edilmese bile uygulanmalı.

## 6) Hızlı doğrulama

```bash
curl -s -X POST http://127.0.0.1:8080/api/v1/device/robocat-1/sync \
  -H 'Content-Type: application/json' \
  -H 'X-Device-Key: <key>' \
  -d '{"rssi":-60,"battery_v":11.8,"events":[{"type":"name_called"}]}' | jq
curl -s http://127.0.0.1:8080/api/v1/devices | jq
```
