import os
from PIL import Image, ImageOps


for fn in os.listdir('./products'):
    name, ext = os.path.splitext(fn)
    if ext != '.jpg':
        continue
    print(name)
    img = Image.open('./products/' + fn)
    img = img.convert('RGB')
    # image 1
    img.save(f'./products2/{name}-1.png')
    # image 2
    ImageOps.grayscale(img).save(f'./products2/{name}-2.png')
    # image 3
    ImageOps.posterize(img, 2).save(f'./products2/{name}-3.png')
    # image 4
    ImageOps.invert(img).save(f'./products2/{name}-4.png')
