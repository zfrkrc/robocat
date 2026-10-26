# RoboCat — görev ve etkileşim davranışı

Bu belge **davranış sözleşmesidir**: sunucu hangi durumda hangi komutu üretir, hangi olayla geçer. Sunucu hareket denetleyicisi değildir; komutları kuyruğa yazar, robot uygular ve `ack` verir.

> **Deterministik kural:** Hiçbir geçiş rastgele değildir. Her geçiş (a) açık bir olay, (b) bir zaman aşımı veya (c) sabit bir eşik ile olur. Aynı girdi → aynı çıktı.

## 1) Durumlar

| Durum | Ne olur | Çıkış |
|---|---|---|
| `follow` | Robot **seni takip eder** (yerel döngü). Sunucu sürekli tanıma yapmaz. | `env_check` / süre dolunca `scan` |
| `scan` | Robot **durur**, çevre kontrolü için kare yükler | kanıt varsa `wait_answer`, yoksa `follow` |
| `hold` | İsimle seslenildi: durur, "Efendim?" | `resume` veya `name_called`/`env_check` |
| `wait_answer` | Selam + "Alkol testi ister misin?" (8 s) | `answer` (evet/hayır) veya süre aşımı |
| `alcohol_test` | **Burun uzatılır**, MQ-3 ölçümü beklenir (20 s) | `sensor` veya süre aşımı |
| `estop` | E-stop açık: yalnız `stop` kabul | e-stop kalkınca `follow` |
| `idle` | Görev yok | `mission/start` |

## 2) Akış (senin tarif ettiğin davranış)

```
follow ──(60 s / çevre kontrolü)──► scan ──(kanıt yok)──► follow
                                     └──(ArUco/kişi ≥2 kare)──► wait_answer
wait_answer ──"hayır" veya 8 s sessizlik──► follow
            └──"evet"──► alcohol_test ──sensör──► sonuç söylenir ──► follow
name_called (her durumda) ──► hold ──"resume"──► follow
e-stop ──► estop (her şey durur) ──kaldırılınca──► follow
```

### Adım adım
1. **Varsayılan: takip.** Kamera sürekli tanıma yapmaz; sadece `scan` anında kare yüklenir.
2. **Çevre kontrolü:** 60 s'de bir veya sensörler "dur ve bak" dediğinde robot `hold` eder, 2–3 kare yükler.
3. **Tanıma (deterministik):** aynı etiket **en az 2 karede** tekrar etmeli. Hareketli bölge tek başına kişi sayılmaz. Kanıt yoksa "unknown" → takibe dön (rastgele tanışma yok).
4. **Tanışma:** `stop` + yüze bak (`look`) + "Merhaba, ben RoboCat." + "Alkol testi ister misin?"
5. **Cevap beklenir (8 s):**
   - **Evet** → `nose_extend` + "Burnumu uzatıyorum, üfleyin." → sensör (20 s).
   - **Hayır** → "Tanıştığıma memnun oldum." → takip.
   - **Cevap yok** → hayır sayılır.
6. **Sonuç:** ham değer + kaba bant söylenir, `nose_retract`, takibe dönülür.
7. **İsimle seslenme:** her durumda `stop` + "Efendim?" → `hold`. "resume" ya da yeni olayla devam.
8. **E-stop:** sunucu tarafı kapı; `stop` dışındaki komutlar 409. Gerçek güvenlik robot üstündeki yerel stop.

## 3) Komut sözlüğü (sunucu → robot)

| `kind` | `params` | Anlam |
|---|---|---|
| `follow` | `{}` | yerel takip döngüsünü başlat |
| `hold` | `{}` | dur, pozisyonu koru |
| `stop` | `{}` | acil dur (yerel stop ile aynı) |
| `look` | `{"pan":0,"tilt":0}` | başı hedefe çevir |
| `say` | `{"text":"..."}` | TTS / seslendirme (metin sunucudan) |
| `nose_extend` | `{}` | burnu uzat (gaz sensörü ölçüm pozisyonu) |
| `nose_retract` | `{}` | burnu geri çek |
| `greet` | `{}` | selam hareketi |
| `move` | `{"linear":0.1,"strafe":0,"rotate":0}` | kısa manevra |
| `calibrate` | `{}` | yerel kalibrasyon |

## 4) Zamanlamalar (env)

| Değişken | Varsayılan | Anlam |
|---|---|---|
| `ROBO_ENV_CHECK_S` | 60 | takipte çevre kontrolü aralığı |
| `ROBO_SCAN_TIMEOUT_S` | 10 | tarama sonucu bekleme |
| `ROBO_ANSWER_TIMEOUT_S` | 8 | soruya cevap bekleme |
| `ROBO_SENSOR_TIMEOUT_S` | 20 | gaz ölçümü bekleme |

## 5) Alkol ölçümü — dürüst sınır

- MQ-3 **kalibre edilmemiştir**; sonuç **hukuki veya tıbbi ölçüm değildir**.
- Rapor: ham değer (`ppm` veya `mV`) + kaba bant (`dusuk`/`orta`/`yuksek`).
- Eşikler kodda sabittir: ppm 80/200, mV 1500/2500. Kalibrasyon yordamı ve gerçek eşikler **henüz yok**.
- Sensör ısıtıcısı ~800 mW; burun içine yerleştirilmeden önce ısıl ayrım ve havalandırma gerekir.

## 6) Tanıma kuralları (rastgelelik yok)

| Kanıt | Kabul | Kimlik |
|---|---|---|
| ArUco işaretçi ≥2 karede | ✅ | `marker_<id>` |
| YOLO `person` ≥2 karede, ortalama skor ≥0.35 | ✅ (model varsa) | `person` |
| Sadece hareket (MOG2) | ❌ | — |
| Tek kare | ❌ | — |
| Operatörün `person_seen` olayı | ✅ (varlık) | `person_seen` |

API: `GET /api/v1/robots/{id}/recognize?camera_id=...` (karar) · `POST /api/v1/robots/{id}/mission/scan?camera_id=...` (karar + göreve işle).

## 7) Açık işler

- Yüz/kimlik tanıma **yok** (planlanmadı); kimlik için ArUco kart veya operatör onayı.
- Sesle isim çağırma: sunucu metin olayı bekler (`name_called`); **konuşma tanıma yerelde** yapılmalı.
- TTS: sunucu metni üretir; seslendirme yerelde (robot üstünde) çalınır.
- MQ-3 kalibrasyonu, burun mekanizması (`nose_extend`) ve sensör ısıl tasarımı henüz yok.
