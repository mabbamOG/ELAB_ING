import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from utilities import loadiconbutton,loadalbumimage

class Album():
	def __init__(self):
		pass
	def get_album(self, id, name, artist, year, image, size='big', type='grid'):
		if type == 'grid':


class GridAlbum(Gtk.Box):
    def __init__(self, id, name, artist, year, image, size):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, homogeneous=False)
        image_label = loadalbumimage(image, size)
        name_label = Gtk.Label(f'<i>{name}</i>', use_markup=True, hexpand=True)
        artist_label = Gtk.Label(artist, hexpand=True)
        year_label = Gtk.Label(year, hexpand=True)

        self.add(image_label)
        self.add(name_label)
        self.add(artist_label)
        self.add(year_label)

class ListAlbum(Gtk.Grid):
    def __init__(self, id, name, artist, year, image, size):
        Gtk.Grid.__init__(self)
        image_label = loadalbumimage(image, size)
        name_label = Gtk.Label(f'<i>{name}</i>', use_markup=True, hexpand=True)
        artist_label = Gtk.Label(artist, hexpand=True)
        year_label = Gtk.Label(year, hexpand=True)

        self.attach(image_label,0,0,1,2)
        self.attach_next_to(name_label,image_label,Gtk.PositionType.RIGHT,3,1)
        self.attach_next_to(artist_label,name_label,Gtk.PositionType.BOTTOM,2,1)
        self.attach_next_to(year_label,artist_label,Gtk.PositionType.RIGHT,1,1)
