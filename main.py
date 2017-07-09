#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from utilities import loadiconbutton

import signal
import json
import albuminfo
from album import ListAlbum,GridAlbum
import cart



        


class Catalogo(Gtk.ScrolledWindow):
    def __init__(self, database, shopping_cart):
        self.shopping_cart = shopping_cart
        self.database = database
        Gtk.ScrolledWindow.__init__(self)
        catalogo = Gtk.FlowBox(homogeneous=True, max_children_per_line=5, min_children_per_line=2, orientation=Gtk.Orientation.HORIZONTAL, selection_mode=Gtk.SelectionMode.NONE)
        for id, album in database.items():
            item = GridAlbum(id, image=album['image'], name=album['name'], artist=album['artist'], year=album['year'])
            but = Gtk.Button()
            but.add(item)
            but.id = id
            but.connect('clicked', self.on_click_album)
            catalogo.add(but)
        self.add(catalogo)

    def on_click_album(self, widget):
        print('you clicked album #',widget.id,'with artist: ',self.database[widget.id]['artist'])
        infowindow =  albuminfo.Window(self.database[widget.id])
        result = infowindow.run()
        print(f'added to cart {result} copies for the album {widget.id}')
        if result >0:
            old_amount = self.shopping_cart.get(widget.id, 0)
            self.shopping_cart[widget.id] = old_amount + result




class Window(Gtk.Window):
    def __init__(self, album_database, shopping_cart):
        Gtk.Window.__init__(self, title="Music Market", border_width=10, default_width=300, default_height=300)

        self.album_database = album_database
        self.shopping_cart = shopping_cart

        # handle titlebar
        self.titlebar = Gtk.HeaderBar(title="Music Market", subtitle="like Amazon but for music", show_close_button=True)
        self.set_titlebar(self.titlebar)

        grid_button = loadiconbutton('th-large','white')
        bars_button = loadiconbutton('bars','white')
        refresh_button = loadiconbutton('refresh','white')
        refresh_button.connect('clicked', self.on_refresh)
        cart_button = loadiconbutton('shopping-cart', 'white')
        cart_button.connect('clicked', self.on_view_cart)
        login_button = loadiconbutton('sign-in', 'white')
        self.search = Gtk.SearchEntry(text='search here')
        #self.search.connect...

        search_selector = Gtk.ComboBoxText()
        search_selector.append_text('album')
        search_selector.append_text('artista')
        search_selector.append_text('canzone')
        search_selector.set_active(0)

        self.titlebar.pack_end(grid_button)
        self.titlebar.pack_end(bars_button)
        self.titlebar.pack_end(cart_button)
        self.titlebar.pack_end(login_button)
        self.titlebar.pack_start(refresh_button)
        self.titlebar.pack_start(self.search)
        self.titlebar.pack_start(search_selector)

        # handle content
        # album_database = { str(i):{'name':'Amerikkas Most Wanted', 'artist':'Ice Cube', 'year':'2009', 'month':'12', 'image':str(i), 'genre':'rap', 'description':'such cool stuff from Ice Cube!', 'songs':['A','B','C'], 'price':'14.99' } for i in range(200)}
        self.add(Catalogo(self.album_database, self.shopping_cart))
        
    def on_view_cart(self, widget):
        print('redirecting to cart...')
        cartwindow = cart.Window(self.album_database, self.shopping_cart)
        cartwindow.show_all()


    def on_refresh(self, widget):
        print('refreshing catalogue...')
        None # loady thingy
        album_database = None 
        self.get_child().destroy()
        self.add(Catalogo(album_database))
        self.show_all()



with open('/home/mad/Documents/000/ELAB-ING/database.json') as f:
    s = f.read()
    database = json.loads(s)

shopping_cart = {}
app = Window(database, shopping_cart)
app.connect("delete-event", Gtk.main_quit)
app.show_all()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
