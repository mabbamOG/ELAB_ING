import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from utilities import loadiconbutton
import network

class Window(Gtk.Window):
    def __init__(self, shopping_cart):
        Gtk.Window.__init__(self, title='Payment', border_width=10, default_width=300, default_height=300, modal=True)
        titlebar = Gtk.HeaderBar(title='Payment', subtitle="please follow instructions", show_close_button=True)
        self.set_titlebar(titlebar)
        self.add(PaymentInfo(shopping_cart))
        self.show_all()
        self.connect('delete-event', Gtk.main_quit)
        self.errors = self.get_child().errors
        Gtk.main()


class PaymentInfo(Gtk.Box):
    def __init__(self, shopping_cart):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.shopping_cart = shopping_cart
        self.errors = False

        self.purchase_methods = Gtk.ComboBoxText()
        self.purchase_methods.append_text('CREDIT CART')
        self.purchase_methods.append_text('BANCOMAT')
        self.purchase_methods.append_text('PAYPAL')
        self.purchase_methods.set_active(0)
        self.shipping_methods = Gtk.ComboBoxText()
        self.shipping_methods.append_text('POST')
        self.shipping_methods.append_text('COURIER')
        self.shipping_methods.set_active(0)
        pay_button = loadiconbutton('arrow-circle-o-right', 'black')
        pay_button.connect('clicked', self.on_pay)

        self.add(Gtk.Label('PURCHASE METHOD:'))
        self.add(self.purchase_methods)
        self.add(Gtk.Label('SHIPPING METHOD:'))
        self.add(self.shipping_methods)
        self.add(pay_button)

    def on_pay(self, widget):
        data = {'cart':self.shopping_cart.copy(), 'purchase_method':self.purchase_methods.get_active_text(), 'shipping_method':self.shipping_methods.get_active_text()}
        conn = network.Network('localhost', 9999)
        pay_ok = conn.pay(data)
        self.shopping_cart.clear()
        if not pay_ok:
            print('purchase not ok')
            self.errors = True
            self.shopping_cart.update(data['cart'])
        else:
            print('purchase ok')
        Gtk.main_quit()
