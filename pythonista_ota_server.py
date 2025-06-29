# Pythonista用 OTAサーバー＆ダウンロードスクリプト
# PCのLive Serverからfirmware.binをダウンロードし、
# その後、iPhone上でHTTPサーバーを起動してESP32に提供します。

import requests
import http.server
import socketserver
import os
import threading
import time

# --- ユーザー設定項目 ---
# お使いの環境に合わせて、以下のIPアドレスを必ず設定してください。

# 1. PCのTailscale IPアドレス
#    Windowsのタスクトレイアイコン等で確認できる 100.x.x.x 形式のアドレス
PC_TAILSCALE_IP = "YOUR_PC_TAILSCALE_IP"

# 2. iPhoneのHTTPサーバーが使用するポート
#    通常は8000で問題ありませんが、他のアプリと競合する場合は変更してください。
IPHONE_SERVER_PORT = 8000

# ------------------------

# --- 固定設定項目 (通常は変更不要) ---
PC_LIVE_SERVER_PORT = 5500
PC_FIRMWARE_PATH = "/firmware/firmware.bin"
PC_FIRMWARE_URL = f"http://{PC_TAILSCALE_IP}:{PC_LIVE_SERVER_PORT}{PC_FIRMWARE_PATH}"

# iPhone上でfirmware.binを保存し、HTTPサーバーが公開するディレクトリ
# PythonistaのDocumentsフォルダ直下を想定しています。
# 必要に応じて変更してください。
# 例: 'esp_ota_iphone' のようにサブフォルダを指定することも可能です。
IPHONE_LOCAL_DIR = os.path.expanduser('~/Documents') # PythonistaのDocumentsフォルダ

# ダウンロードしたfirmware.binの保存パス
LOCAL_FIRMWARE_PATH = os.path.join(IPHONE_LOCAL_DIR, 'firmware.bin')
# ------------------------------------

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=IPHONE_LOCAL_DIR, **kwargs)

def download_firmware():
    print(f"Downloading firmware from PC: {PC_FIRMWARE_URL}")
    try:
        # 保存先ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(LOCAL_FIRMWARE_PATH), exist_ok=True)

        response = requests.get(PC_FIRMWARE_URL, timeout=30)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生
        
        with open(LOCAL_FIRMWARE_PATH, 'wb') as f:
            f.write(response.content)
        
        print(f"Successfully downloaded firmware to: {LOCAL_FIRMWARE_PATH}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Failed to download firmware from PC: {e}")
        print("Please check the following:")
        print("1. Is Live Server running on your PC?")
        print(f"2. Is the PC Tailscale IP '{PC_TAILSCALE_IP}' correct?")
        print("3. Is your PC and iPhone connected to Tailscale?")
        return False
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred during file operation: {e}")
        return False

def start_http_server():
    # 現在の作業ディレクトリをHTTPサーバーの公開ディレクトリに設定
    os.chdir(IPHONE_LOCAL_DIR)
    
    with socketserver.TCPServer(("", IPHONE_SERVER_PORT), CustomHandler) as httpd:
        print(f"\n--- iPhone HTTP Server Started ---")
        print(f"Serving firmware.bin from: {IPHONE_LOCAL_DIR}")
        print(f"Access URL for ESP32: http://<iPhoneのIP>:{IPHONE_SERVER_PORT}/firmware.bin")
        print(f"Server running on port {IPHONE_SERVER_PORT}. Press Ctrl+C to stop.")
        httpd.serve_forever()

if __name__ == "__main__":
    # まずファームウェアをダウンロード
    if download_firmware():
        # ダウンロードが成功したらHTTPサーバーを起動
        start_http_server()
    else:
        print("\nFirmware download failed. HTTP server will not start.")