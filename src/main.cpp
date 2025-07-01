#include <M5Unified.h> 
#include <WiFi.h>
#include <HTTPClient.h>
#include <Update.h>

const char* ssid = "YOUR SSID";  // テザリングのSSID
const char* password = "YOUR PASS";  // パスワード

const char* firmware_url = "http://172.20.10.1:8000/firmware.bin";  // PythonistaサーバのURL

bool wifiConnected = false;

void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);
  M5.Display.setTextSize(2);
  M5.Display.println("Booting...");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED && retries < 20) {
    delay(500);
    M5.Display.print(".");
    retries++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    M5.Display.println("\nWiFi Connected");
    M5.Display.println(WiFi.localIP());
    M5.Display.println("Press BtnA for OTA");
  } else {
    wifiConnected = false;
    M5.Display.println("\nWiFi Failed");
  }
}

void doOTA() {
  M5.Display.println("Starting OTA...");

  HTTPClient http;
  http.begin(firmware_url);
  int httpCode = http.GET();

  if (httpCode == HTTP_CODE_OK) {
    int contentLength = http.getSize();
    WiFiClient* stream = http.getStreamPtr();

    if (!Update.begin(contentLength)) {
      M5.Display.println("No space for OTA");
      return;
    }

    size_t written = Update.writeStream(*stream);

    if (written == contentLength) {
      M5.Display.println("OTA written OK");
    } else {
      M5.Display.printf("OTA partial: %d/%d\n", written, contentLength);
    }

    if (Update.end()) {
      if (Update.isFinished()) {
        M5.Display.println("OTA Done. Reboot.");
        delay(2000);
        ESP.restart();
      } else {
        M5.Display.println("OTA not finished");
      }
    } else {
      M5.Display.printf("OTA error: %d\n", Update.getError());
    }
  } else {
    M5.Display.printf("HTTP error: %d\n", httpCode);
  }

  http.end();
}

void loop() {
  M5.update();

  // ボタンAを押したときにOTAを実行
  if (wifiConnected && M5.BtnA.wasPressed()) {
    doOTA();
  }

  if(M5.BtnB.wasPressed()){
    M5.Display.println("hello, button B");
  }

  if(M5.BtnC.wasPressed()){
    M5.Display.clear();
  }

  delay(100);
}
