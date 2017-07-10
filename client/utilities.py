import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import os

scriptpath = os.path.dirname(os.path.realpath(__file__))

def button_decorator(func):
    def func_wrapper(*data):
        return Gtk.Button(image=func(*data), expand=False)
    return func_wrapper

def loadicon(path, size):
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(path, width=size, height=size)
    img = Gtk.Image.new_from_pixbuf(pixbuf)
    img.set_hexpand(False)
    return img

@button_decorator
def loadiconbutton(s, color):
    filepath = f'{scriptpath}/../icons/{color}/{str(s).strip()}.svg'
    return loadicon(filepath, 50)

def loadalbumimage(s, size):
    filepath = f'{scriptpath}/../album_images/{str(s).strip()}.jpg'
    size = 150 if size=='big' else 50 if size=='small' else 0
    return loadicon(filepath, size)
