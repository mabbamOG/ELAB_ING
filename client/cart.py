import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from utilities import loadiconbutton
import decimal
from album import ListAlbum
import purchase
import login

class Window(Gtk.Window):
    def __init__(self, album_database, shopping_cart, account):
        Gtk.Window.__init__(self, title='Shopping Cart', border_width=10, default_width=300, default_height=300, modal=True)
        titlebar = Gtk.HeaderBar(title='Shopping Cart', subtitle='your pre-purchase overview', show_close_button=True)
        self.set_titlebar(titlebar)
        self.shopping_cart = shopping_cart
        self.close = False
        self.add(CartInfo(album_database, self.shopping_cart, account))
        self.get_child().errors = False

    def quit(self, widget, event):
        self.close = True
        Gtk.main_quit()

    def run(self):
        self.show_all()
        self.connect('delete-event', self.quit)
        print(f'child is {self.get_child()}')
        Gtk.main()
        if self.close or (not self.shopping_cart and not self.get_child().errors):
            return True
        else:
            return False



class CartInfo(Gtk.Box):
    def __init__(self, album_database, shopping_cart, account):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.errors = False
        self.shopping_cart = shopping_cart
        self.album_database = album_database
        self.account = account
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
            amountinput.id = key
            amountinput.connect('value-changed', self.on_change_value)
            delete_button = loadiconbutton('trash','black')
            delete_button.set_vexpand(False)
            delete_button.set_hexpand(False)
            delete_button.id = key
            delete_button.box = box
            delete_button.connect('clicked', self.on_delete_entry)

            box.add(ListAlbum(key,name,artist,year,image,size='small'))
            box.add(price_label)
            box.add(amountinput)
            box.add(delete_button)
            self.add(box)

        # self.add(Gtk.Label(str(self.shopping_cart)))

        # final price and purchase button
        self.total_price = 0
        self.purchase_label = Gtk.Label('', use_markup=True)
        self.purchase_button = loadiconbutton('usd','black')
        self.purchase_button.connect('clicked', self.on_purchase)
        self.update_total()
        purchase_box = Gtk.Box(halign=Gtk.Align.CENTER)
        purchase_box.add(self.purchase_label)
        purchase_box.add(self.purchase_button)

        self.add(purchase_box)

    def update_total(self):
        self.total_price = sum(value*decimal.Decimal(self.album_database[key]['price']) for key,value in self.shopping_cart.items())
        self.purchase_label.set_markup(f'<big><big>TOTAL PRICE: <b>{self.total_price}</b></big></big>')
        print(self.shopping_cart)
        if not self.shopping_cart:
            self.purchase_button.set_sensitive(False)


    def on_change_value(self, widget):
        new_value = widget.get_value_as_int()
        self.shopping_cart[widget.id] = new_value
        self.update_total()

    def on_delete_entry(self, widget):
        del self.shopping_cart[widget.id]
        self.update_total()
        widget.box.destroy()

    def on_purchase(self, widget):
        print('attempting purchase...')
        if self.shopping_cart:
            if not self.account:
                print('(side) logging in...')
                loginwindow = login.Window(self.account)
            if self.account:
                purchasewindow = purchase.Window(self.shopping_cart)
                self.errors = purchasewindow.errors
                purchasewindow.destroy()
                Gtk.main_quit()
        else:
            print('cart is empty!')
