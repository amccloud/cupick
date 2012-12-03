import ImageFilter

def blur(im, blur=False, **kwargs):
    if blur:
        im = im.filter(ImageFilter.BLUR)

    return im
