import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class Window(Gtk.Window):
    def __init__(self, album_database, shopping_cart):
        Gtk.Window.__init__(self, title='Payment', border_width=10, default_width=300, default_height=300, modal=True)
        titlebar = Gtk.HeaderBar(title='Payment', subtitle="please follow instructions", show_close_button=True)
        self.set_titlebar(titlebar)

        self.add(CartInfo(album_database, shopping_cart))


class CartInfo(Gtk.Box):
    def __init__(self, album_database, shopping_cart):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.shopping_cart = shopping_cart
