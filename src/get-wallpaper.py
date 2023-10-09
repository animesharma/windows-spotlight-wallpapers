import os
import shutil

from tqdm import tqdm  # Import tqdm for the progress bar
from PIL import Image  # Import the Python Imaging Library (PIL)

# Get the user's profile directory
user_profile = os.path.expandvars(r"%userprofile%")
SPOTLIGHT_DIR = os.path.join(user_profile, "AppData", "Local", "Packages", "Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy", "LocalState", "Assets")
WALLPAPER_DIR = r"D:\Wallpapers"
MIN_WIDTH = 1280  # Minimum width in pixels
MIN_HEIGHT = 720  # Minimum height in pixels

if not os.path.exists(WALLPAPER_DIR):
    os.makedirs(WALLPAPER_DIR)

# List all files in SPOTLIGHT_DIR
spotlight_files = os.listdir(SPOTLIGHT_DIR)

# Initialize tqdm with the total number of files
with tqdm(total=len(spotlight_files), desc="Copying files") as pbar:
    for filename in spotlight_files:
        src_file = os.path.join(SPOTLIGHT_DIR, filename)
        dst_file = os.path.join(WALLPAPER_DIR, filename + ".jpg")

        # Get the base filename (without extension)
        base_filename, _ = os.path.splitext(filename)

        # Check if the file already exists in the destination
        if not os.path.exists(dst_file):
            try:
                # Open the image and get its dimensions
                img = Image.open(src_file)
                width, height = img.size
                # Check if dimensions meet the minimum requirements
                if width >= MIN_WIDTH and height >= MIN_HEIGHT:
                    # Copy the file
                    shutil.copy2(src=src_file, dst=dst_file)  
                else:
                    print(f"Skipping {filename} (dimensions too small)")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

        # Update the progress bar
        pbar.update(1)
