# resize_batch_minimal.py
import os
from PIL import Image, ImageOps

# --- CONFIG ---
INPUT_DIR = "input_images"    # folder with original images
OUTPUT_DIR = "output_images"  # folder to save resized images
MAX_SIZE = (800, 600)         # (width, height) max bounding box
JPEG_QUALITY = 90             # quality for JPEG saves (1-100)
# ---------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

for fname in os.listdir(INPUT_DIR):
    in_path = os.path.join(INPUT_DIR, fname)
    out_path = os.path.join(OUTPUT_DIR, fname)

    # skip directories and hidden files
    if not os.path.isfile(in_path) or fname.startswith("."):
        continue

    try:
        with Image.open(in_path) as img:
            # respect EXIF orientation (rotated phone photos)
            img = ImageOps.exif_transpose(img)

            # create a thumbnail that fits inside MAX_SIZE while keeping aspect ratio
            img.thumbnail(MAX_SIZE, Image.LANCZOS)

            # JPEG can't store alpha, convert if needed
            fmt = (img.format or fname.split(".")[-1]).upper()
            if fmt in ("JPEG", "JPG"):
                if img.mode in ("RGBA", "LA"):
                    img = img.convert("RGB")
                img.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
            else:
                # PNG, GIF, WEBP keep transparency
                img.save(out_path)

            print(f"Saved: {out_path}  (size={img.size})")
    except Exception as e:
        print(f"Skipping {in_path}: {e}")
