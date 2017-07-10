import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import os

scriptpath = os.path.dirname(os.path.realpath(__file__))
def loadiconbutton(s, color):
    filepath = f'{scriptpath}/../icons/{color}/{str(s).strip()}.svg'
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filepath, width=50, height=50)
    img = Gtk.Image.new_from_pixbuf(pixbuf)
    but = Gtk.Button(image=img, expand=False)
    return but

def loadalbumimage(s, size):
    filepath = f'{scriptpath}/../album_images/{str(s).strip()}.jpg'
    size = 150 if size=='big' else 50 if size=='small' else 0
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filepath, width=size, height=size)
    img = Gtk.Image.new_from_pixbuf(pixbuf)
    img.set_hexpand(False)
    return img
