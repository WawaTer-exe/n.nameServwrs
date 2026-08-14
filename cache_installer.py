import os
import zipfile
import shutil

def setup_custom_cache():
    # Detect the game directory
    target_dir = os.path.join("RecRoom_Data", "CustomCache")
    
    print("=======================================================")
    print("        REBORNREC CACHE INSTALLATION UTILITY          ")
    print("=======================================================")
    
    # 1. Create the folder if it's missing
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"[Info] Created empty map cache directory at: {target_dir}")
    else:
        print(f"[Info] Found existing cache directory at: {target_dir}")
        
    # 2. Check if the user downloaded a map pack zip file
    zip_name = "maps_cache.zip" # The filename they should name their downloaded map archive
    
    if os.path.exists(zip_name):
        print(f"[Success] Found {zip_name}! Extracting assets...")
        try:
            with zipfile.ZipFile(zip_name, 'r') as zip_ref:
                # Extract directly into RecRoom_Data/CustomCache
                zip_ref.extractall(target_dir)
            print("[Success] All historical 2018-2019 game maps have been successfully injected!")
            print("You can now safely walk into Paintball, Laser Tag, and Quest doors.")
        except Exception as e:
            print(f"[Error] Failed to extract map files: {e}")
    else:
        print("\n[Action Required] No map archive found!")
        print(f"Please download the 2018/2019 map cache zip file from your trusted archive,")
        print(f"rename it to '{zip_name}', place it in this folder, and run this script again.")
        print("-------------------------------------------------------")
        print("Without these files, moving to an activity will cause an infinite loading screen.")

if __name__ == "__main__":
    setup_custom_cache()
