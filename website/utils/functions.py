from flask import flash
from PIL import Image

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(error, 'error')


def is_truthy(string: str) -> bool:
    return string.lower() in ["tak", "t", "yes", "y", "1"]

def comments(self, userid):
        return Comment.query.filter_by(to=userid)

def crop_image(dir):
    image = Image.open(dir)
    width, height = image.size
    if width == height:
        return image
    offset  = int(abs(height-width)/2)
    if width>height:
        image = image.crop([offset,0,width-offset,height])
    else:
        image = image.crop([0,offset,width,height-offset])
    new_size = (300, 300)
    image = image.resize(new_size)

    image.save(dir)