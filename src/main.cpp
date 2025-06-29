#include <M5Unified.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Update.h>

const char* ssid = "YOUR_SSID";  // テザリングのSSID
const char* password = "YOUR_PASSWORD";  // パスワード

const char* firmware_url = "http://172.20.10.1:8000/firmware.bin";  // PythonistaサーバのURL

void setup() {
  auto cfg = M5.config();       // M5Stack初期設定用の構造体を代入
  M5.begin(cfg);
  // Serial.begin(115200);
  M5.Display.setTextSize(3);               // テキストサイズを変更
  M5.Display.print("Hello M5 with gemini");       // 画面にHello M5 with geminiと1行表示
  M5.Display.print("ok");
  Serial.println("hello m5stack with gemini");         // シリアルモニターにhello m5stack with geminiと1行表示

  delay(1000);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (++retries > 20) {
      Serial.println("\nWiFi connection failed");
      ESP.restart();
    }
  }

  Serial.println("\nConnected to WiFi");
  Serial.println("IP Address: ");
  Serial.println(WiFi.localIP());

  // HTTP OTA 開始
  Serial.println("Starting OTA update...");

  HTTPClient http;
  http.begin(firmware_url);
  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK) {
    int contentLength = http.getSize();
    WiFiClient* stream = http.getStreamPtr();

    if (!Update.begin(contentLength)) {
      Serial.println("Not enough space to begin OTA");
      return;
    }

    size_t written = Update.writeStream(*stream);

    if (written == contentLength) {
      Serial.println("Written : " + String(written) + " successfully");
    } else {
      Serial.println("Written only : " + String(written) + "/" + String(contentLength) + ". Retry?");
    }

    if (Update.end()) {
      Serial.println("OTA done!");
      if (Update.isFinished()) {
        Serial.println("Update successfully completed. Rebooting.");
        ESP.restart();
      } else {
        Serial.println("Update not finished? Something went wrong!");
      }
    } else {
      Serial.println("Error Occurred. Error #: " + String(Update.getError()));
    }
  } else {
    Serial.println("Cannot download firmware. HTTP code: " + String(httpCode));
  }

  http.end();
}

void loop() {
  M5.update();
  // M5.Display.print("hello m5");
  delay(1000);
  // Do nothing
}
