import os
import shutil
import logging
from PIL import Image
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Constants
USER_PROFILE = Path.home()
SPOTLIGHT_DIR = USER_PROFILE / "AppData" / "Local" / "Packages" / "Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy" / "LocalState" / "Assets"
WALLPAPER_DIR = Path("D:/Wallpapers")
MIN_WIDTH_PX, MIN_HEIGHT_PX = 1280, 720  # Minimum dimensions in pixels

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
    if dst_file.is_file():
        return

    try:
        # Open the image and get its dimensions
        with Image.open(src_file) as img:
            width, height = img.size

        # Check if dimensions meet the minimum requirements
        if width < MIN_WIDTH_PX or height < MIN_HEIGHT_PX:
            logging.warning(f"Skipping {entry.name} (dimensions too small)")
            return

        # Copy the file
        shutil.copy2(src_file, dst_file)
    except Exception as e:
        logging.error(f"Error processing {entry.name}: {e}")

def main() -> None:
    """Main function to process all files."""
    setup_directory(WALLPAPER_DIR)

    spotlight_files = (entry for entry in os.scandir(SPOTLIGHT_DIR) if entry.is_file())
    total_files: int = sum(1 for f in os.scandir(SPOTLIGHT_DIR) if f.is_file())

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_file, entry): entry for entry in spotlight_files}
        for _ in tqdm(as_completed(futures), total=total_files, desc="Copying files"):
            pass

if __name__ == "__main__":
    main()
