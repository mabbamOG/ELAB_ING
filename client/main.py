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
import login

class Catalogo(Gtk.ScrolledWindow):
    def __init__(self, album_database, shopping_cart, grid=True):
        Gtk.ScrolledWindow.__init__(self)
        self.shopping_cart = shopping_cart
        self.album_database = album_database
        if grid:
            self.catalogo = Gtk.FlowBox(homogeneous=True, max_children_per_line=5, min_children_per_line=2, orientation=Gtk.Orientation.HORIZONTAL, selection_mode=Gtk.SelectionMode.NONE)
        else:
            self.catalogo = Gtk.ListBox(selection_mode = Gtk.SelectionMode.NONE)
        self.catalogo.set_sort_func(self.sort_by_name)
        self.catalogo.set_filter_func(self.filter_by_name)
        for id, album in album_database.items():
            if grid:
                item = GridAlbum(id, image=album['image'], name=album['name'], artist=album['artist'], year=album['year'])
            else:
                item = ListAlbum(id, image=album['image'], name=album['name'], artist=album['artist'], year=album['year'])
            but = Gtk.Button()
            but.add(item)
            but.id = id
            but.connect('clicked', self.on_click_album)
            self.catalogo.add(but)
        self.add(self.catalogo)

    def on_click_album(self, widget):
        print('you clicked album #',widget.id,'with artist: ',self.album_database[widget.id]['artist'])
        infowindow =  albuminfo.Window(self.album_database[widget.id])
        result = infowindow.run()
        print(f'added to cart {result} copies for the album {widget.id}')
        if result >0:
            old_amount = self.shopping_cart.get(widget.id, 0)
            self.shopping_cart[widget.id] = old_amount + result

    def sort_by_name(self, child1, child2, data=None):
        id1, id2 = child1.get_child().id, child2.get_child().id
        a, b = self.album_database[id1]['name'], self.album_database[id2]['name']
        return (a > b) - (a < b)

    def filter_by_name(self, child, data=''):
        id = child.get_child().id
        reference = self.album_database[id]['name']
        if data.islower():
            reference = reference.lower()
        return data in reference
    def filter_by_artist(self, child, data=''):
        id = child.get_child().id
        reference = self.album_database[id]['artist']
        if data.islower():
            reference = reference.lower()
        return data in reference
    def filter_by_song(self, child, data=''):
        id = child.get_child().id
        for song in self.album_database[id]['songs']:
            if data.islower():
                song = song.lower()
            print(song)
            if data in song:
                return True
        return False

    def update_filter(self, mode, s):
        if mode == 'album':
            self.catalogo.set_filter_func(self.filter_by_name, s)
        elif mode == 'artist':
            self.catalogo.set_filter_func(self.filter_by_artist, s)
        elif mode == 'song':
            self.catalogo.set_filter_func(self.filter_by_song, s)
        else:
            raise 'filter update error!'
        self.catalogo.invalidate_filter()



class Window(Gtk.Window):
    def __init__(self, album_database, shopping_cart, account):
        Gtk.Window.__init__(self, title="Music Market", border_width=10, default_width=1000, default_height=600)
        self.connect("delete-event", Gtk.main_quit)
        self.account = account

        self.album_database = album_database
        self.shopping_cart = shopping_cart

        # handle titlebar
        self.titlebar = Gtk.HeaderBar(title="Music Market", subtitle="like Amazon but for music", show_close_button=True)
        self.set_titlebar(self.titlebar)

        grid_button = loadiconbutton('th-large','white')
        grid_button.connect('clicked', self.on_grid_view)
        bars_button = loadiconbutton('bars','white')
        bars_button.connect('clicked', self.on_list_view)
        refresh_button = loadiconbutton('refresh','white')
        refresh_button.connect('clicked', self.on_refresh)
        cart_button = loadiconbutton('shopping-cart', 'white')
        cart_button.connect('clicked', self.on_view_cart)
        self.login_button = loadiconbutton('key', 'white')
        self.login_button.connect('clicked', self.on_login)
        self.logout_button = loadiconbutton('sign-out','white')
        self.logout_button.connect('clicked', self.on_logout)
        self.search = Gtk.SearchEntry(placeholder_text='search here', max_length=30)
        self.search.connect('changed', self.on_search)

        self.search_selector = Gtk.ComboBoxText()
        self.search_selector.append_text('album')
        self.search_selector.append_text('artist')
        self.search_selector.append_text('song')
        self.search_selector.set_active(0)

        self.titlebar.pack_end(grid_button)
        self.titlebar.pack_end(bars_button)
        self.titlebar.pack_end(cart_button)
        self.titlebar.pack_end(self.login_button)
        self.titlebar.pack_end(self.logout_button)
        self.titlebar.pack_start(refresh_button)
        self.titlebar.pack_start(self.search)
        self.titlebar.pack_start(self.search_selector)

        # handle content
        self.view = Catalogo(self.album_database, self.shopping_cart)
        self.add(self.view)
        self.show_all()
        self.logout_button.hide()
        
    def on_grid_view(self, widget):
        self.remove(self.view)
        self.view = Catalogo(self.album_database, self.shopping_cart, grid=True)
        self.view.show_all()
        self.add(self.view)

    def on_list_view(self, widget):
        self.remove(self.view)
        self.view = Catalogo(self.album_database, self.shopping_cart, grid=False)
        self.view.show_all()
        self.add(self.view)


    def on_view_cart(self, widget):
        print('redirecting to cart...')
        cartwindow = cart.Window(self.album_database, self.shopping_cart, self.account)
        ok = cartwindow.run()
        cartwindow.destroy()
        if not ok:
            self.on_view_cart(widget)
        if self.account:
            self.login_button.hide()
            self.logout_button.show()


    def on_login(self, widget):
        print('logging in...')
        loginwindow = login.Window(self.account)
        if self.account:
            self.login_button.hide()
            self.logout_button.show()

    def on_logout(self, widget):
        print('logging out..')
        self.account.clear()
        self.login_button.show()
        self.logout_button.hide()

    def on_refresh(self, widget):
        print('refreshing catalogue...')
        None # loady thingy
        album_database = None 
        self.get_child().destroy()
        self.add(Catalogo(album_database))
        self.show_all()

    def on_search(self, widget):
        text = self.search.get_text()
        print(f'searching for {text}...')
        mode = self.search_selector.get_active_text()
        self.get_child().update_filter(mode, text)


        




with open('/home/mad/Documents/000/ELAB-ING/client/database.json') as f:
    s = f.read()
    database = json.loads(s)

shopping_cart = {}
account = {}
app = Window(database, shopping_cart, account)
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
