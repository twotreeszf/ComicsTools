#!/usr/bin/env python3
"""
Convert all images in a given directory to JPG format.
The original files are replaced with JPG versions, keeping the same base filename.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}


def convert_image_to_jpg(image_path: Path) -> bool:
    """
    Convert an image to JPG format. 
    Returns True if conversion was performed, False if skipped.
    """
    suffix = image_path.suffix.lower()
    output_path = image_path.with_suffix(".jpg")
    
    # If already .jpg, check if mode conversion is needed
    if suffix == ".jpg" or suffix == ".jpeg":
        return True
    
    # Convert other formats to JPG
    try:
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        elif img.mode != "RGB":
            img = img.convert("RGB")
        
        img.save(output_path, "JPEG", quality=85)
        img.close()
        
        # Remove original file
        image_path.unlink()
        print(f"  Converted: {image_path.name} -> {output_path.name}")
        return True
        
    except Exception as e:
        print(f"  Warning: Failed to convert {image_path.name}: {e}")
        return False


def convert_images_in_directory(folder_path: str) -> None:
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    if not folder.is_dir():
        print(f"Error: Not a directory: {folder_path}")
        sys.exit(1)
    
    # Find all image files in the folder
    image_files = [
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]
    
    if not image_files:
        print(f"No images found in folder: {folder_path}")
        return
    
    # Sort by filename
    image_files.sort(key=lambda p: p.name)
    
    print(f"Found {len(image_files)} images in folder...")
    
    converted_count = 0
    for image_file in image_files:
        if convert_image_to_jpg(image_file):
            converted_count += 1
    
    print(f"\nDone! Converted {converted_count} images.")


def main():
    parser = argparse.ArgumentParser(
        description="Convert all images in a directory to JPG format."
    )
    parser.add_argument(
        "folder",
        help="Path to the folder containing images"
    )
    
    args = parser.parse_args()
    convert_images_in_directory(args.folder)


if __name__ == "__main__":
    main()

