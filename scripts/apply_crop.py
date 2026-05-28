
from PIL import Image
import json

IMAGE_PATH = r"g:\My Drive\Research\Revell\07a Articles\07a.27 - Lxx Mt Aspects\07a.27_p1_300dpi.png"
CROP_PATH = r"g:\My Drive\Research\Revell\07a Articles\07a.27 - Lxx Mt Aspects\07a.27_p1_cropped.png"
BOUNDS = {"ymin": 139, "xmin": 366, "ymax": 940, "xmax": 716}

def crop_image(path, output_path, bounds):
    img = Image.open(path)
    width, height = img.size

    # Coordinates are normalized 0-1000
    left = bounds['xmin'] * width / 1000
    top = bounds['ymin'] * height / 1000
    right = bounds['xmax'] * width / 1000
    bottom = bounds['ymax'] * height / 1000

    print(f"Original size: {width}x{height}")
    print(f"Cropping to: {left}, {top}, {right}, {bottom}")

    cropped_img = img.crop((left, top, right, bottom))
    cropped_img.save(output_path)
    print(f"Saved cropped image to {output_path}")

if __name__ == "__main__":
    crop_image(IMAGE_PATH, CROP_PATH, BOUNDS)
