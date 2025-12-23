#!/usr/bin/env python3
"""
Convert images in a folder to a PDF file.
The PDF file will be named after the folder and saved in the same parent directory.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tiff"}


def images_to_pdf(folder_path: str) -> None:
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
        print(f"Error: No images found in folder: {folder_path}")
        sys.exit(1)
    
    # Sort by filename to ensure consistent ordering
    image_files.sort(key=lambda p: p.name)
    
    print(f"Found {len(image_files)} images in folder...")
    
    # Output PDF path: same parent directory, folder name as filename
    output_pdf = folder.parent / f"{folder.name}.pdf"
    
    # Load and convert images
    images: list[Image.Image] = []
    for image_file in image_files:
        try:
            img = Image.open(image_file)
            # Convert to RGB if necessary (PDF doesn't support RGBA)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            elif img.mode != "RGB":
                img = img.convert("RGB")
            images.append(img)
            print(f"  Loaded: {image_file.name}")
        except Exception as e:
            print(f"  Warning: Failed to load {image_file.name}: {e}")
    
    if not images:
        print("Error: No valid images to convert.")
        sys.exit(1)
    
    # Save as PDF
    first_image = images[0]
    remaining_images = images[1:] if len(images) > 1 else []
    
    first_image.save(
        output_pdf,
        "PDF",
        save_all=True,
        append_images=remaining_images,
        resolution=100.0
    )
    
    # Close all images
    for img in images:
        img.close()
    
    print(f"\nDone! Created PDF: {output_pdf}")
    print(f"Total pages: {len(images)}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert images in a folder to a PDF file."
    )
    parser.add_argument(
        "folder",
        help="Path to the folder containing images"
    )
    
    args = parser.parse_args()
    images_to_pdf(args.folder)


if __name__ == "__main__":
    main()

