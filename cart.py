import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from utilities import loadiconbutton
import decimal
from album import ListAlbum

class Window(Gtk.Window):
    def __init__(self, album_database, shopping_cart):
        Gtk.Window.__init__(self, title='Shopping Cart', border_width=10, default_width=300, default_height=300, modal=True)
        titlebar = Gtk.HeaderBar(title='Shopping Cart', subtitle='your pre-purchase overview', show_close_button=True)
        self.set_titlebar(titlebar)

        self.add(CartInfo(album_database, shopping_cart))


class CartInfo(Gtk.Box):
    def __init__(self, album_database, shopping_cart):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.shopping_cart = shopping_cart
        self.album_database = album_database
        # list of cart items
        for key,value in self.shopping_cart.items():
            box = Gtk.Box(homogeneous=False)
            name = self.album_database[key]['name']
            artist = self.album_database[key]['artist']
            year = self.album_database[key]['year']
            image = self.album_database[key]['image']
            price = self.album_database[key]['price']
            price_label = Gtk.Label(f'<big><u><b>{price}$</b></u></big>', use_markup=True)

            amountinput = Gtk.SpinButton.new_with_range(1,100,1)
            amountinput.set_vexpand(False)
            amountinput.set_hexpand(False)
            amountinput.set_value(value)
            amountinput.connect('value-changed', lambda w: self.on_change_value(w,key))
            delete_button = loadiconbutton('trash','black')
            delete_button.set_vexpand(False)
            delete_button.set_hexpand(False)
            delete_button.connect('clicked', lambda w: self.on_delete_entry(w, key, box))

            box.add(ListAlbum(key,name,artist,year,image,size='small'))
            box.add(price_label)
            box.add(amountinput)
            box.add(delete_button)
            self.add(box)

        # self.add(Gtk.Label(str(self.shopping_cart)))

        # final price and purchase button
        self.total_price = 0
        self.purchase_label = Gtk.Label('', use_markup=True)
        self.update_total()
        purchase_button = loadiconbutton('usd','black')
        purchase_button.connect('clicked', self.on_purchase)
        purchase_box = Gtk.Box(halign=Gtk.Align.CENTER)
        purchase_box.add(self.purchase_label)
        purchase_box.add(purchase_button)

        self.add(purchase_box)

    def update_total(self):
        self.total_price = sum(value*decimal.Decimal(self.album_database[key]['price']) for key,value in self.shopping_cart.items())
        self.purchase_label.set_markup(f'<big><big>TOTAL PRICE: <b>{self.total_price}</b></big></big>')
        self.show_all()


    def on_change_value(self, widget, id):
        new_value = widget.get_value_as_int()
        self.shopping_cart[id] = new_value
        self.update_total()

    def on_delete_entry(self, widget, id, daddy):
        del self.shopping_cart[id]
        self.update_total()
        daddy.destroy()

    def on_purchase(self, widget):
        print('attempting purchase...')
        # purchasewindow = purchase.Window()
        # purchasewindow.show_all()

