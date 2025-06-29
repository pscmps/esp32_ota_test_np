import os
import shutil
Import("env")

def copy_firmware_bin(source, target, env):
    """ビルド後にfirmware.binをプロジェクトルートにコピーする"""
    firmware_path = os.path.join(env.PioEnv().get("BUILD_DIR"), "firmware.bin")
    project_dir = env.PioEnv().get("PROJECT_DIR")
    target_path = os.path.join(project_dir, "firmware.bin")

    if os.path.exists(firmware_path):
        print(f"Copying {firmware_path} to {target_path}")
        shutil.copyfile(firmware_path, target_path)
        print("Copying done.")
    else:
        print(f"Error: {firmware_path} not found.")

# ビルド完了のアクションとして関数を登録
env.AddPostAction("$BUILD_DIR/firmware.bin", copy_firmware_bin)
