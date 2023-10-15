import os
import shutil
from PIL import Image
from tqdm import tqdm

# Constants
USER_PROFILE = os.path.expandvars(r"%userprofile%")
SPOTLIGHT_DIR = os.path.join(USER_PROFILE, "AppData", "Local", "Packages", "Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy", "LocalState", "Assets")
WALLPAPER_DIR = r"D:\Wallpapers"
MIN_WIDTH, MIN_HEIGHT = 1280, 720  # Minimum dimensions in pixels

# Create the wallpaper directory if it doesn't exist
os.makedirs(WALLPAPER_DIR, exist_ok=True)

# Get all files in SPOTLIGHT_DIR
spotlight_files = os.listdir(SPOTLIGHT_DIR)

# Initialize tqdm with the total number of files
with tqdm(total=len(spotlight_files), desc="Copying files") as pbar:
    for filename in spotlight_files:
        src_file = os.path.join(SPOTLIGHT_DIR, filename)
        dst_file = os.path.join(WALLPAPER_DIR, f"{filename}.jpg")

        # Skip if the file already exists in the destination
        if os.path.exists(dst_file):
            pbar.update(1)
            continue

        try:
            # Open the image and get its dimensions
            with Image.open(src_file) as img:
                width, height = img.size

            # Check if dimensions meet the minimum requirements
            if width < MIN_WIDTH or height < MIN_HEIGHT:
                print(f"Skipping {filename} (dimensions too small)")
                pbar.update(1)
                continue

            # Copy the file
            shutil.copy2(src=src_file, dst=dst_file)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

        # Update the progress bar
        pbar.update(1)
