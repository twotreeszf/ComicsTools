#!/usr/bin/env python3
"""
Resize all images in a directory (including subfolders) to a given width while maintaining aspect ratio.
The resized images are saved as JPG format, replacing the original files.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}


def resize_image(image_path: Path, base_folder: Path, target_width: int) -> bool:
    """
    Resize an image to the target width while maintaining aspect ratio.
    Always resize to target width regardless of original size.
    Returns True if resize was performed, False if failed.
    """
    output_path = image_path.with_suffix(".jpg")
    relative_path = image_path.relative_to(base_folder)
    
    try:
        img = Image.open(image_path)
        original_width, original_height = img.size
        
        # Calculate new height maintaining aspect ratio
        ratio = target_width / original_width
        target_height = int(original_height * ratio)
        
        # Resize image
        img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Convert to RGB if needed
        if img_resized.mode in ("RGBA", "P"):
            img_resized = img_resized.convert("RGB")
        elif img_resized.mode != "RGB":
            img_resized = img_resized.convert("RGB")
        
        img_resized.save(output_path, "JPEG", quality=85)
        img_resized.close()
        img.close()
        
        # Remove original file if different from output
        if image_path != output_path:
            image_path.unlink()
        
        print(f"  Resized: {relative_path} ({original_width}x{original_height} -> {target_width}x{target_height})")
        return True
        
    except Exception as e:
        print(f"  Warning: Failed to process {relative_path}: {e}")
        return False


def resize_images_in_directory(folder_path: str, target_width: int) -> None:
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"Error: Folder not found: {folder_path}")
        sys.exit(1)
    
    if not folder.is_dir():
        print(f"Error: Not a directory: {folder_path}")
        sys.exit(1)
    
    # Find all image files in the folder and subfolders recursively
    image_files = [
        f for f in folder.rglob("*")
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]
    
    if not image_files:
        print(f"No images found in folder: {folder_path}")
        return
    
    # Sort by full path
    image_files.sort(key=lambda p: str(p))
    
    print(f"Found {len(image_files)} images in folder (including subfolders)...")
    print(f"Target width: {target_width}px\n")
    
    processed_count = 0
    for image_file in image_files:
        if resize_image(image_file, folder, target_width):
            processed_count += 1
    
    print(f"\nDone! Processed {processed_count} images.")


def main():
    parser = argparse.ArgumentParser(
        description="Resize all images in a directory to a given width while maintaining aspect ratio."
    )
    parser.add_argument(
        "folder",
        help="Path to the folder containing images"
    )
    parser.add_argument(
        "width",
        type=int,
        help="Target width in pixels"
    )
    
    args = parser.parse_args()
    
    if args.width <= 0:
        print("Error: Width must be a positive integer.")
        sys.exit(1)
    
    resize_images_in_directory(args.folder, args.width)


if __name__ == "__main__":
    main()

