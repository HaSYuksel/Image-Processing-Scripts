from PIL import Image
import os
from io import BytesIO
import warnings

def compress_image(input_path, output_path, target_size_kb=1000):
    """Compresses an image by resizing and reducing quality iteratively until the file size is under the target size or the minimum quality is reached."""
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', Image.DecompressionBombWarning)
        img = Image.open(input_path)

    img_format = img.format  # Preserve the original image format
    initial_size_kb = os.path.getsize(input_path) / 1024

    # More aggressive resizing based on initial assessment
    factor = (target_size_kb / initial_size_kb) ** 0.5
    factor = max(factor, 0.5)  # Avoid too small a factor which might overly degrade the image
    new_width = int(img.width * factor)
    new_height = int(img.height * factor)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Adjust quality dynamically
    quality = 95
    while quality > 10:
        img_bytes = BytesIO()
        img.save(img_bytes, format=img_format, quality=quality, optimize=True)
        size_kb = img_bytes.tell() / 1024

        if size_kb <= target_size_kb:
            img.save(output_path, format=img_format, quality=quality, optimize=True)
            print(f"Saved {output_path} at quality {quality}, size {size_kb:.2f}KB")
            return
        quality -= 5  # Decrease quality stepwise

    # Final save if target size not met
    img.save(output_path, format=img_format, quality=10, optimize=True)
    final_size_kb = img_bytes.tell() / 1024
    print(f"Saved {output_path} at minimum quality, size {final_size_kb:.2f}KB")

def compress_images(source_dir, output_dir, formats=('JPEG', 'JPG', 'PNG', 'WEBP')):
    """Compresses all images in a directory below a specified size."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(source_dir):
        if filename.split('.')[-1].upper() in formats:
            file_path = os.path.join(source_dir, filename)
            output_file_path = os.path.join(output_dir, filename)
            compress_image(file_path, output_file_path)

# Set your source and output directory
source_directory = 'D:/UhCLASSWebDev/compression test'
output_directory = 'D:/UhCLASSWebDev/done test'

# Call the function to compress images
compress_images(source_directory, output_directory)
