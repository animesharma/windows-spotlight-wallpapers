import os
import shutil
import logging
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Constants
USER_PROFILE = Path.home()
SPOTLIGHT_DIR = USER_PROFILE / "AppData" / "Local" / "Packages" / "Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy" / "LocalState" / "Assets"
WALLPAPER_DIR = Path("D:/Wallpapers")
MIN_WIDTH, MIN_HEIGHT = 1280, 720  # Minimum dimensions in pixels

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_directory(directory: Path) -> None:
    """Create the directory if it doesn't exist."""
    directory.mkdir(parents=True, exist_ok=True)

def process_file(entry: os.DirEntry[str]) -> None:
    """Process a single file."""
    src_file = Path(entry.path)
    dst_file = WALLPAPER_DIR / f"{entry.name}.jpg"

    # Skip if the file already exists in the destination
    if dst_file.exists():
        return

    try:
        # Open the image and get its dimensions
        with Image.open(src_file) as img:
            width, height = img.size

        # Check if dimensions meet the minimum requirements
        if width > MIN_WIDTH and height > MIN_HEIGHT:
            # Copy the file
            shutil.copy2(src_file, dst_file)
        else:
            logging.warning(f"Skipping {entry.name} (dimensions too small)")
    except Exception as e:
        logging.error(f"Error processing {entry.name}: {e}")

def main() -> None:
    """Main function to process all files."""
    setup_directory(WALLPAPER_DIR)

    with os.scandir(SPOTLIGHT_DIR) as entries:
        spotlight_files = list(entries)

        with ThreadPoolExecutor() as executor:
            for _ in tqdm(executor.map(process_file, spotlight_files), total=len(spotlight_files), desc="Copying files"):
                pass

if __name__ == "__main__":
    main()
