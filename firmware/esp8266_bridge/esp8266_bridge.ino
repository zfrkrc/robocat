/*
 * RoboCat ESP8266 köprüsü — sunucu ile tek turda senkron.
 *
 *   POST /api/v1/device/{DEVICE_ID}/sync      (X-Device-Key)
 *   -> {"commands":[{id,kind,params}], "next_poll_s":2, "config":{...}}
 *
 * Her turda: durum gönder (rssi/batarya/sensör), olayları ilet, komutları
 * al, uygula, sonucu bir sonraki turda "ack" olarak bildir.
 *
 * Gerekli kütüphaneler: ESP8266WiFi, ESP8266HTTPClient, ArduinoJson 7.
 * NOT: Bu bir referans iskelettir; servo/DFPlayer uygulamaları TODO'dur.
 */
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#if USE_TLS
#include <WiFiClientSecure.h>
#endif
#include <ArduinoJson.h>

// ---- yapılandırma -------------------------------------------------
static const char *WIFI_SSID = "CHANGE_ME";
static const char *WIFI_PASS = "CHANGE_ME";
// Üretim: https://esp32.zk.net.tr  (Cloudflare tüneli, TLS edge'de biter)
// LAN testi: http://<sunucu-ip>:8090
static const char *SERVER_URL = "https://esp32.zk.net.tr";
#define USE_TLS 1                       // 1 = WiFiClientSecure, 0 = düz HTTP
static const char *DEVICE_ID  = "robocat-1";
static const char *DEVICE_KEY = "CHANGE_ME";                  // ROBO_DEVICE_KEYS ile aynı

static const uint32_t MIN_POLL_MS = 1500;     // sunucu 429 derse bunu büyüt
static uint32_t nextPollMs = 2000;

// ---- durum --------------------------------------------------------
struct PendingAck { int id; bool ok; const char *note; };
static PendingAck acks[6];
static uint8_t ackCount = 0;

static uint32_t lastPoll = 0;

void queueAck(int id, bool ok, const char *note = nullptr) {
  if (ackCount < 6) acks[ackCount++] = {id, ok, note};
}

// ---- komut uygulama (TODO: gerçek donanım) -------------------------
void applyCommand(int id, const char *kind, JsonObject params) {
  if (!strcmp(kind, "follow"))        { Serial.println(F("[cmd] follow")); queueAck(id, true); }
  else if (!strcmp(kind, "hold"))     { Serial.println(F("[cmd] hold"));   queueAck(id, true); }
  else if (!strcmp(kind, "stop"))     { Serial.println(F("[cmd] STOP"));   queueAck(id, true); }
  else if (!strcmp(kind, "look"))     { Serial.printf("[cmd] look pan=%d\n", (int)(params["pan"] | 0)); queueAck(id, true); }
  else if (!strcmp(kind, "say"))      { Serial.printf("[cmd] say: %s\n", (const char*)(params["text"] | "")); queueAck(id, true); }
  else if (!strcmp(kind, "nose_extend"))  { Serial.println(F("[cmd] nose_extend"));  queueAck(id, true); }
  else if (!strcmp(kind, "nose_retract")) { Serial.println(F("[cmd] nose_retract")); queueAck(id, true); }
  else if (!strcmp(kind, "move"))     { Serial.println(F("[cmd] move"));   queueAck(id, true); }
  else if (!strcmp(kind, "greet"))    { Serial.println(F("[cmd] greet"));  queueAck(id, true); }
  else if (!strcmp(kind, "idle"))     { Serial.println(F("[cmd] idle"));   queueAck(id, true); }
  else { Serial.printf("[cmd] bilinmeyen: %s\n", kind); queueAck(id, false, "unknown"); }
}

// ---- tek tur ------------------------------------------------------
void syncOnce() {
  if (WiFi.status() != WL_CONNECTED) return;

  StaticJsonDocument<1024> req;   // ArduinoJson 7: JsonDocument req;
  req["ts"]   = (uint32_t)millis() / 1000;
  req["rssi"] = WiFi.RSSI();
  req["firmware"] = "esp8266-bridge-0.1";

  JsonObject sensors = req.createNestedObject("sensors");
  sensors["current_a"] = 0.0;      // TODO: ACS712
  sensors["pitch"]     = 0.0;      // TODO: MPU6050

  JsonArray events = req.createNestedArray("events");
  // Örnek: isim çağrısı yerel mikrofon/LCD butonundan geliyorsa:
  // JsonObject ev = events.createNestedObject(); ev["type"] = "name_called";

  JsonArray ackArr = req.createNestedArray("ack");
  for (uint8_t i = 0; i < ackCount; i++) {
    JsonObject a = ackArr.createNestedObject();
    a["id"] = acks[i].id; a["ok"] = acks[i].ok;
    if (acks[i].note) a["note"] = acks[i].note;
  }
  ackCount = 0;   // gönderdik; sunucu kabul etmezse komut TTL ile düşer

  String body; serializeJson(req, body);

#if USE_TLS
  WiFiClientSecure client;
  client.setInsecure();          // TODO: setTrustAnchors() veya setFingerprint() ile sabitle
  client.setBufferSizes(1024, 512);
#else
  WiFiClient client;
#endif
  HTTPClient http;
  http.setTimeout(4000);
  String url = String(SERVER_URL) + "/api/v1/device/" + DEVICE_ID + "/sync";
  if (!http.begin(client, url)) return;
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-Device-Key", DEVICE_KEY);

  int code = http.POST(body);
  if (code == 200) {
    JsonDocument res;                       // ArduinoJson 7
    if (!deserializeJson(res, http.getString())) {
      nextPollMs = (uint32_t)((res["next_poll_s"] | 2.0f) * 1000.0f);
      for (JsonObject c : res["commands"].as<JsonArray>()) {
        applyCommand(c["id"] | 0, c["kind"] | "", c["params"].as<JsonObject>());
      }
    }
  } else if (code == 429) {
    nextPollMs = min(nextPollMs * 2, 15000u);
  } else if (code == 401) {
    Serial.println(F("401: DEVICE_KEY hatali"));
    nextPollMs = 10000;
  } else {
    nextPollMs = min(nextPollMs + 1000, 15000u);
  }
  http.end();
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.hostname(DEVICE_ID);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  uint8_t tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries++ < 40) delay(500);
  Serial.printf("IP: %s\n", WiFi.localIP().toString().c_str());
}

void loop() {
  uint32_t now = millis();
  if (now - lastPoll >= max(nextPollMs, MIN_POLL_MS)) {
    lastPoll = now;
    syncOnce();
  }
  delay(20);
}

/*
 * TLS notu (Cloudflare):
 *   - esp32.zk.net.tr Cloudflare proxy'li; TLS edge'de sonlanır, origin'e HTTP gider.
 *   - ESP8266 BearSSL TLS 1.2 destekler; 2 sn'de bir sync için yeterli ama RAM/CPU pahalı.
 *   - setInsecure() yalnız geliştirme içindir. Üretimde Cloudflare sertifikasını
 *     setTrustAnchors() ile sabitle (kök değişimi nadirdir) veya kısa ömürlü fingerprint kullan.
 */
