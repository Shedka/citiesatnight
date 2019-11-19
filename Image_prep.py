from resizeimage import resizeimage
from PIL import Image
import numpy as np

def format(image, size):
    # import and convert to grayscale
    img = Image.open(image).convert('LA')
    # adapt size
    w, h = size
    cover = resizeimage.resize_cover(img, [w, h])
    # change to MNIST data structure
    Matrix = [[cover.getpixel((x, y))[0] for x in range(w)] for y in range(h)]
    return Matrix

def save(Matrix, filename):
    # save with int format
    f = filename + ".csv"
    np.savetxt(f, Matrix, fmt='%3.0f')

img_names = ["Ref_Tokyo_grayscale.jpg", "Tokyo_grayscale.jpg", "Sapporo_grayscale.jpg"]
for image in img_names:
    save(format(image, [32, 32]),image)














