from PIL import Image
from resizeimage import resizeimage
import os

# Resize list image
def resize_list_image(filepath):
    filepath = 'static/assets/' + filepath
    filename, file_extension = os.path.splitext(filepath)
    with open(filepath, 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [40, 40])
            cover.save(filename+"_40x40"+file_extension, image.format)
            cover = resizeimage.resize_cover(image, [60, 60])
            cover.save(filename+"_60x60"+file_extension, image.format)
            cover = resizeimage.resize_cover(image, [130, 130])
            cover.save(filename+"_130x130"+file_extension, image.format)
    return
    
