import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from utilities import loadiconbutton,loadalbumimage

class Info(Gtk.Box):
    def __init__(self, key, value, alternate=False):
        Gtk.Box.__init__(self)
        key_label = Gtk.Label(f'<b>{key.upper()}:</b>', halign=Gtk.Align.START, use_markup=True)
        value_label = Gtk.Label(value, halign=Gtk.Align.END)
        if alternate:
            value_label.set_markup(f'<i>{value_label.get_text()}</i>')
            value_label.set_line_wrap(True)
        
        self.pack_start(key_label, expand=True, fill=True, padding=10)
        self.pack_start(value_label, expand=True, fill=True, padding=10)

class AlbumInfo(Gtk.Box):
    def __init__(self, album):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.CENTER)
        songs = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.CENTER)
        for i, title in enumerate(album['songs'], 1):
            songs.add(Info(str(i), title))
        albumimage = loadalbumimage(album['image'], 'big')
        topbox = Gtk.Box()
        topbox.pack_start(albumimage, expand=True, fill=True, padding=10)
        topbox.pack_start(songs, expand=True, fill=True, padding=10)
        self.add(topbox)
        self.add(Info('price', album['price']+'$'))
        self.add(Info('artist', album['artist']))
        self.add(Info('date', album['month']+'/'+album['year']))
        self.add(Info('genre', album['genre']))
        self.add(Info('description', album['description'], alternate=True))
        

        self.numberinput = Gtk.SpinButton.new_with_range(1, 100, 1)
        cart_button = loadiconbutton('cart-plus', 'black')
        cart_button.connect('clicked', self.on_add_cart)

        purchasebox = Gtk.Box(halign=Gtk.Align.CENTER)
        purchasebox.add(self.numberinput)
        purchasebox.add(cart_button)

        self.add(purchasebox)
        self.result=0

    def on_add_cart(self, widget):
        self.result = self.numberinput.get_value_as_int()
        Gtk.main_quit()



class Window(Gtk.Window):
    def __init__(self, album):
        Gtk.Window.__init__(self, title=album['name'], border_width=10, default_width=300, default_height=300, modal=True)
        titlebar = Gtk.HeaderBar(title=album['name'], subtitle=album['artist'], show_close_button=True)

        self.set_titlebar(titlebar)
        self.info = AlbumInfo(album)
        self.add(self.info)
        self.connect('delete-event', Gtk.main_quit)

    def run(self):
        self.show_all()
        Gtk.main()
        self.destroy()
        return self.info.result
