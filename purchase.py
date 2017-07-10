import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from utilities import loadiconbutton

class Window(Gtk.Window):
    def __init__(self, shopping_cart):
        Gtk.Window.__init__(self, title='Payment', border_width=10, default_width=300, default_height=300, modal=True)
        titlebar = Gtk.HeaderBar(title='Payment', subtitle="please follow instructions", show_close_button=True)
        self.set_titlebar(titlebar)
        self.add(PaymentInfo(shopping_cart))
        self.show_all()
        self.connect('delete-event', Gtk.main_quit)
        Gtk.main()


class PaymentInfo(Gtk.Box):
    def __init__(self, shopping_cart):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.shopping_cart = shopping_cart

        purchase_methods = Gtk.ComboBoxText()
        purchase_methods.append_text('CARTA DI CREDITO')
        purchase_methods.append_text('BANCOMAT')
        purchase_methods.append_text('PAYPAL')
        purchase_methods.set_active(0)
        shipping_methods = Gtk.ComboBoxText()
        shipping_methods.append_text('POSTA')
        shipping_methods.append_text('CORRIERE')
        shipping_methods.set_active(0)
        pay_button = loadiconbutton('arrow-circle-o-right', 'black')
        pay_button.connect('clicked', self.on_pay)

        self.add(Gtk.Label('PURCHASE METHOD:'))
        self.add(purchase_methods)
        self.add(Gtk.Label('SHIPPING METHOD:'))
        self.add(shipping_methods)
        self.add(pay_button)

    def on_pay(self, widget):
        self.shopping_cart.clear()
        if network:
            self.shopping_cart.update(network)
        Gtk.main_quit()
