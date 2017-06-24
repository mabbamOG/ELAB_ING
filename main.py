import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import signal

def loadiconbutton(s):
    filepath = 'assets/'+str(s).strip()+'.svg'
    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(filepath, width=50, height=50)
    img = Gtk.Image.new_from_pixbuf(pixbuf)
    but = Gtk.Button(image=img)
    return but


class Album(Gtk.Box):
    def __init__(self, name, artist, year, image):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.add(Gtk.Label(image))
        self.add(Gtk.Label(name))
        self.add(Gtk.Label(artist))
        self.add(Gtk.Label(year))


class Catalogo(Gtk.ScrolledWindow):
    def __init__(self):
        Gtk.ScrolledWindow.__init__(self)
        catalogo = Gtk.FlowBox(max_children_per_line=5, min_children_per_line=2, orientation=Gtk.Orientation.HORIZONTAL, selection_mode=Gtk.SelectionMode.NONE)
        for i in range(200):
            item = Album(image=f'{i}:', name='Amerikkkas Most Wanted', artist='Ice Cube', year='2009')
            but = Gtk.Button()
            but.add(item)
            but.connect('clicked', self.on_click_album)
            catalogo.add(but)
        self.add(catalogo)

    def on_click_album(self, widget):
        print('you clicked',widget)



class App(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Music Market", border_width=10, default_width=300, default_height=300)
        titlebar = Gtk.HeaderBar(title="Music Market", subtitle="like Amazon but for music", show_close_button=True)

        titlebar.pack_end(loadiconbutton('th-large'))
        titlebar.pack_end(loadiconbutton('bars'))
        titlebar.pack_start(loadiconbutton('refresh'))
        search = Gtk.SearchEntry(text='hi')
        searchchoices = Gtk.ComboBoxText()
        searchchoices.append_text('album')
        searchchoices.append_text('artista')
        searchchoices.append_text('canzone')
        searchchoices.set_active(0)
        titlebar.pack_start(search)
        titlebar.pack_start(searchchoices)

        self.set_titlebar(titlebar)
        self.add(Catalogo())


app = App()
app.connect("delete-event", Gtk.main_quit)
app.show_all()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
