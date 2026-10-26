# RoboCat — internete açık dağıtım (Cloudflare Tunnel)

**Durum (2026-10-27):** yayında.
`https://esp32.zk.net.tr` → Cloudflare (TLS edge) → **ayrı** tünel → `127.0.0.1:8090` (FastAPI).
Üretim tüneli (`insightmap`, 3742f166…) **değiştirilmedi**.

## Bileşenler

| Bileşen | Yer | Not |
|---|---|---|
| `robocat-server.service` | systemd | `uvicorn` 127.0.0.1:8090, `Restart=always` |
| `/etc/robocat/server.env` | chmod 600 | veri dizini + cihaz anahtarları |
| `robocat-tunnel.service` | systemd | `cloudflared` ayrı tünel (`robocat`) |
| `/etc/cloudflared/robocat.yml` | — | yalnız `esp32.zk.net.tr` + catch-all 404 |
| DNS | Cloudflare API | `esp32.zk.net.tr` CNAME → `<tunnel>.cfargotunnel.com`, proxied |
| Veri | `/var/lib/robocat` | SQLite + kareler |

Kurulum dosyaları: [`deploy/`](../deploy).

## Neden ayrı tünel
Üretim tüneli **uzaktan (dashboard) yönetiliyor**; yerel `config.yml` yazımları geçersiz kalıyor.
Ayrı tünel ile RoboCat kendi yerel yapılandırmasını kullanır ve diğer siteleri etkilemez.

## Kontrol

```bash
systemctl status robocat-server robocat-tunnel
curl -s https://esp32.zk.net.tr/api/v1/health | jq
sudo journalctl -u robocat-server -n 30 --no-pager
sudo journalctl -u robocat-tunnel -n 30 --no-pager
```

Cihaz testi (anahtar `/etc/robocat/server.env` içinde):

```bash
KEY=$(grep -o 'robocat-1:.*' /etc/robocat/server.env | cut -d: -f2-)
curl -s -X POST https://esp32.zk.net.tr/api/v1/device/robocat-1/sync \
  -H "X-Device-Key: $KEY" -H 'Content-Type: application/json' \
  -d '{"rssi":-60,"battery_v":11.8}' | jq
```

## Anahtar yenileme / cihaz ekleme

```bash
NEW=$(python3 -c "import secrets;print(secrets.token_urlsafe(24))")
sudo sed -i "s|^ROBO_DEVICE_KEYS=.*|ROBO_DEVICE_KEYS=robocat-1:$NEW|" /etc/robocat/server.env
sudo systemctl restart robocat-server
```
Çoklu cihaz: `ROBO_DEVICE_KEYS="robocat-1:K1,kol-1:K2"` (virgülle).

## Geri alma

```bash
sudo systemctl disable --now robocat-tunnel robocat-server
cloudflared tunnel delete robocat          # tüneli siler
# DNS kaydını sil: Cloudflare API/panel → esp32.zk.net.tr CNAME
```

## Güvenlik durumu (bilinçli kabul)

- **Kimlik doğrulama yalnız cihaz anahtarı** ile; operatör paneli (`/`, `/docs`) **açık**.
  Dışarıya açık olduğu için paneli kapatmak veya Cloudflare Access eklemek önerilir.
- Cloudflare proxy + TLS edge: trafik uçta şifreli, origin'e tünel içinde gider.
- Cihaz anahtarı sızarsa yalnız o cihaz döndürülür.
- `HTTP` (TLS'siz) yalnız LAN'da kullanılmalı; cihaz `https://` kullanıyor.
- Panel kapatma: `ROBO_DISABLE_DASHBOARD=1` (yol haritasında) — şu an açık.
