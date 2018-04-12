from PIL import Image

def image_center_crop(img_object):
    img_original = Image.open(img_object) # opening image
    # making image compatibale with JPEG FORMAT
    img = Image.new("RGB", img_original.size, (255, 255, 255))
    if img_original.format == 'PNG':
        img.paste(img_original, mask = img_original.split()[3])
    else:
        img = img_original
    
    # cropping to a perfect square
    width, height = img.size
    start = width/2 - height/2
    end = width/2 + height/2
    
    if width != height:
        if width > height:
            crop_region = (start,0,end,height)
        elif width < height:
            crop_region = (0,-start,width,end)
        return img.crop(crop_region)
    else:
        return img

        