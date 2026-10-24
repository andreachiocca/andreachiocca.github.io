"""Create two optimized local WebP sizes from genuine laboratory photographs.

Authoring-only dependency: Pillow. This program is not run by the Jekyll
website or visitor browser.

Run:
python tools/prepare_laboratory_images.py --input /path/to/uploads --output assets/img/laboratory
"""
import argparse
from pathlib import Path
from PIL import Image, ImageOps

SOURCES = {
    "specimen": "IMG_3207.jpeg",
    "structural-bench": "IMG_0167.JPG",
    "schenck-actuators": "IMG_3186.jpeg",
    "steplab-equipment": "IMG_3200.jpeg",
    "rumul": "IMG_3189.jpeg",
    "flir-x6901sc": "IMG_0418.JPG",
    "vibration-setup": "IMG_8745.JPG",
}

def prepare(input_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for slug, name in SOURCES.items():
        if name == "IMG_0420.JPG":
            raise ValueError("Do not publish the FLIR serial-number label photograph")
        source = input_dir / name
        if not source.is_file():
            raise FileNotFoundError(f"Missing genuine laboratory photograph: {source}")
        with Image.open(source) as original:
            image = ImageOps.exif_transpose(original).convert("RGB")
            for width in (640, 1280):
                optimized = image.copy()
                optimized.thumbnail((width, 10000), Image.Resampling.LANCZOS)
                target = output_dir / f"{slug}-{width}.webp"
                optimized.save(target, format="WEBP", quality=74, method=6, exif=b"")
                print(f"{target.name}: {optimized.width}x{optimized.height}, {target.stat().st_size} bytes")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    opts = parser.parse_args()
    prepare(opts.input, opts.output)
