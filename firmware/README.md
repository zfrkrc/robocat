# RoboCat firmware

| Klasör | Ne |
|---|---|
| `esp8266_bridge/` | ESP8266 → sunucu köprüsü (tek tur sync + komut uygulama iskeleti) |

## esp8266_bridge
- Kütüphaneler: `ESP8266WiFi`, `ESP8266HTTPClient`, **ArduinoJson** (6 veya 7).
- `WIFI_SSID`, `WIFI_PASS`, `SERVER_URL`, `DEVICE_ID`, `DEVICE_KEY` alanlarını doldur.
- Sunucuda aynı kimlik: `ROBO_DEVICE_KEYS="robocat-1:<key>"`.
- Döngü: `sync → komutları uygula → ack` (ack bir sonraki turda gider).
- 429 gelirse geri çekilme süresi iki katına çıkar; 401'de anahtarı kontrol et.

Sözleşme: [`docs/DEVICE_PROTOCOL.md`](../docs/DEVICE_PROTOCOL.md).
