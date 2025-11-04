import os
import shutil

# === 1. Create data directory if not exists ===
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# === 2. Local dataset paths ===
LOCAL_IMD_RAINFALL = r"C:\Users\DELL\OneDrive\Desktop\rainfall in india 1901-2015.csv"
LOCAL_CROP_DISTRICT = r"C:\Users\DELL\OneDrive\Desktop\crop_production.csv"

def copy_local_file(src_path, dest_filename):
    """Copy a local file into the project data folder."""
    dest_path = os.path.join(DATA_DIR, dest_filename)
    if not os.path.exists(src_path):
        print(f"❌ File not found: {src_path}")
        return
    shutil.copy(src_path, dest_path)
    print(f"✅ Copied {src_path} → {dest_path}")

if __name__ == "__main__":
    print("=== Starting Data Copy Process ===")

    print("\n📦 Copying IMD Rainfall Data...")
    copy_local_file(LOCAL_IMD_RAINFALL, "imd_rainfall.csv")

    print("\n🌾 Copying Crop Production Data...")
    copy_local_file(LOCAL_CROP_DISTRICT, "crop_district.csv")

    print("\n✅ All datasets have been copied successfully!")
