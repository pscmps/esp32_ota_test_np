### PlatformIO関連コマンド

*   **PIO CLIツールパス:** `C:\Users\YOUR_USERNAME\.platformio\penv\Scripts\pio.exe`
*   **コンパイル:** `C:\Users\YOUR_USERNAME\.platformio\penv\Scripts\pio.exe run`
*   **シリアルモニター:** `C:\Users\YOUR_USERNAME\.platformio\penv\Scripts\pio.exe device monitor`

---

### OTAアップデートの構成概要 (2025/06/28時点)

#### ネットワーク構成

*   **PC:** インターネットに接続し、Tailscale VPNを介してiPhoneから遠隔操作される。
*   **iPhone:** 携帯回線に接続し、Tailscaleを起動。同時に、テザリング機能でプライベートなWi-Fiネットワークを構築する。
*   **ESP32:** iPhoneのテザリングWi-Fiに接続する。このため、ESP32はPCのネットワークには直接アクセスできない。

#### OTAアップデートフロー

1.  **コンパイル (PC):** `pio run` を実行。ビルド後スクリプトにより、`firmware.bin`がプロジェクト直下の`/firmware`フォルダに自動でコピーされる。
2.  **ファイル転送 (PC → iPhone):** PC上の`firmware.bin`を、何らかの方法でiPhoneのPythonistaがアクセスできるローカルフォルダに転送する。
    *   **課題:** この転送プロセスがiCloud同期の不調により煩雑になっている。
3.  **サーバー起動 (iPhone):** iPhoneのPythonistaアプリで、ローカルHTTPサーバーを起動するスクリプトを実行する。
4.  **アップデート実行 (ESP32):** ESP32は、自身の接続するWi-Fiネットワーク内にあるPythonistaのHTTPサーバーにアクセスし、`firmware.bin`をダウンロードしてOTAアップデートを実行する。

#### ESP32の接続情報

*   **Wi-Fi:** iPhoneのテザリング (SSID/パスワードは `src/main.cpp` に記載)
*   **OTAサーバー (iPhone)のIP:** `YOUR_IP_ADDRESS` (Pythonistaが実行されているiPhoneのテzaリングIP)


#### 回答の言語
回答は日本語でお願いします。
---

注意: `src/main.cpp`内のWi-Fiパスワードは、可能な限り既存の値を保持するようにしてください。ただし、新しいコードスニペットがプレースホルダーを含む場合、そのプレースホルダーが使用されます.