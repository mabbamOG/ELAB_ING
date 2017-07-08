import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import os

def loadiconbutton(s, color):
    #filepath = 'icons/'+color+str(s).strip()+'.svg'
    scriptpath = os.path.dirname(os.path.realpath(__file__))
    filepath = f'{scriptpath}/icons/{color}/{str(s).strip()}.svg'
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filepath, width=50, height=50)
    img = Gtk.Image.new_from_pixbuf(pixbuf)
    but = Gtk.Button(image=img)
    return but
