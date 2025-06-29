Import("env")
import os
import shutil

def copy_firmware_to_root(source, target, env):
    firmware_path = target[0].get_abspath()
    destination_dir = os.path.join(env.subst("$PROJECT_DIR"), "firmware")
    
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)
        
    destination_path = os.path.join(destination_dir, "firmware.bin")
    
    print(f'\n--- Copying firmware ---\nSource:      {firmware_path}\nDestination: {destination_path}\n')
    shutil.copyfile(firmware_path, destination_path)
    print("--- Copying complete ---\n")

# Use a more specific target for the post action
env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", copy_firmware_to_root)