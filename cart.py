import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class Window(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title='Shopping Cart', border_width=10, default_width=300, default_height=300, modal=True)
        titlebar = Gtk.HeaderBar(title='Shopping Cart', subtitle='your pre-purchase overview', show_close_button=True)
        self.set_titlebar(titlebar)
        self.add(CartInfo())

class CartInfo(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.add(Gtk.Label('hello world'))
