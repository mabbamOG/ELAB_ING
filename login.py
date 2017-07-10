import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from utilities import loadiconbutton

class GetInfo(Gtk.Box):
    def __init__(self, label, password=False):
        Gtk.Box.__init__(self)
        self.add(Gtk.Label(label, hexpand=True, halign=Gtk.Align.CENTER))
        if password == False:
            self.entry = Gtk.Entry()
        else:
            self.entry = Gtk.Entry(hexpand=False, halign=Gtk.Align.CENTER, caps_lock_warning=True, visibility=False)
        self.add(self.entry)

class Window(Gtk.Window):
    def __init__(self, account):
        Gtk.Window.__init__(self, title='User Account', border_width=10, default_width=300, default_height=300, modal=True)
        titlebar = Gtk.HeaderBar(title='User Account', subtitle='please log in or register', show_close_button=True)
        self.set_titlebar(titlebar)
        self.show_all()
        self.connect('delete-event',Gtk.main_quit)
        self.add(AccountInfo(account))
        Gtk.main()
        self.destroy()

class AccountInfo(Gtk.Box):
    def __init__(self, account):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.account = account
        userbox = GetInfo('USER:')
        passwordbox = GetInfo('PASSWORD:', password=True)

        self.user_entry = userbox.entry
        self.password_entry = passwordbox.entry
        self.checkbutton = Gtk.CheckButton('I wish to register', active=False)
        login_button = loadiconbutton('sign-in','black')
        login_button.set_halign(Gtk.Align.CENTER)
        login_button.set_hexpand(True)
        login_button.set_label('LOG IN')
        register_button = loadiconbutton('user-plus','black')
        register_button.set_hexpand(True)
        register_button.set_halign(Gtk.Align.CENTER)
        register_button.set_label('REGISTER')
        buttonbox = Gtk.Box()
        buttonbox.add(login_button); buttonbox.add(register_button)

        login_button.connect('clicked', self.on_login)
        register_button.connect('clicked', self.on_register)
        self.checkbutton.connect('toggled', self.on_toggle_register)


        self.add(userbox)
        self.add(passwordbox)
        self.add(self.checkbutton)
        self.add(buttonbox)

        self.show_all()
        self.add_hidden()
        self.add_errors()

    def add_errors(self):
        self.user_error = Gtk.Label(f'<span color="red">error: username is missing!</span>', use_markup=True)
        self.password_error = Gtk.Label(f'<span color="red">error: password is missing!</span>', use_markup=True)
        self.password2_error = Gtk.Label(f'<span color="red">error: password confirmation is missing!</span>', use_markup=True)
        self.name_error = Gtk.Label(f'<span color="red">error: name is missing!</span>', use_markup=True)
        self.email_error = Gtk.Label(f'<span color="red">error: email is missing!</span>', use_markup=True)
        self.address_error = Gtk.Label(f'<span color="red">error: address is missing!</span>', use_markup=True)
        self.country_error = Gtk.Label(f'<span color="red">error: data is missing or insufficient!</span>', use_markup=True)

        self.same_password_error = Gtk.Label(f'<span color="red">error: passwords are not the same!</span>', use_markup=True)

        self.add(self.user_error)
        self.add(self.password_error)
        self.add(self.password2_error)
        self.add(self.name_error)
        self.add(self.email_error)
        self.add(self.address_error)
        self.add(self.country_error)
        self.add(self.same_password_error)

    def add_hidden(self):
        password2box = GetInfo('REPEAT PASSWORD:', password=True)
        namebox = GetInfo('Name:')
        emailbox = GetInfo('Email:')
        addressbox = GetInfo('Address:')
        countrybox = GetInfo('Country:')

        self.password2_entry =  password2box.entry
        self.name_entry = namebox.entry
        self.email_entry = emailbox.entry
        self.address_entry = addressbox.entry
        self.country_entry = countrybox.entry

        self.registerbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.registerbox.add(password2box)
        self.registerbox.add(namebox)
        self.registerbox.add(emailbox)
        self.registerbox.add(addressbox)
        self.registerbox.add(countrybox)

        self.add(self.registerbox)

    def empty_check(w1, w2):
        if w1.get_text() == '':
            w2.show()
            return True
        else:
            w2.hide()
            return False

    def login_checks(self):
        empty_check = AccountInfo.empty_check
        if empty_check(self.user_entry, self.user_error): return False
        if empty_check(self.password_entry, self.password_error): return False
        else: return True

    def register_checks(self):
        empty_check = AccountInfo.empty_check
        if not self.login_checks(): return False
        if empty_check(self.password2_entry, self.password2_error): return False
        if empty_check(self.name_entry, self.name_error): return False
        if empty_check(self.email_entry, self.email_error): return False
        if empty_check(self.address_entry, self.address_error): return False
        if empty_check(self.country_entry, self.country_error): return False
        if self.password_entry.get_text() != self.password2_entry.get_text():
            self.same_password_error.show()
            return False
        else:
            self.same_password_error.hide()
            return True

    def on_toggle_register(self, widget):
        if widget.get_active():
            self.registerbox.show_all()
        else:
            self.registerbox.hide()

    def check_empty(self):
        s1, s2 = self.user_entry.get_text(), self.password_entry.get_text()
        if s1 == '' or s2 == '':
            return True
        return False

    def on_login(self, widget):
        self.checkbutton.set_active(False)
        self.on_toggle_register(self.checkbutton)
        check_ok = self.login_checks()
        if check_ok:
            self.account['username'] = self.user_entry.get_text()
            Gtk.main_quit()

    def on_register(self, widget):
        self.on_login(widget)
        if not self.checkbutton.get_active():
            self.checkbutton.set_active(True)
            self.on_toggle_register(self.checkbutton)
            check_ok = self.register_checks()
            if check_ok:
                self.account['username'] = self.user_entry.get_text()
                Gtk.main_quit()


