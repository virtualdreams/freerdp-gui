#!/usr/bin/env python3

import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
import subprocess
import os
import json


class EntryWindow(Gtk.Window):
    def __init__(self):
        # config
        self.config = {}
        self.load_config()

        # init window
        super().__init__(title="FreeRDP GUI")
        self.set_size_request(400, 300)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", self.on_delete_event)

        # main box
        self.mainbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.mainbox)

        # notebook
        self.notebook = Gtk.Notebook()
        self.mainbox.pack_start(self.notebook, True, True, 0)

        # page 1
        self.page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.page1.set_border_width(10)
        self.notebook.append_page(self.page1, Gtk.Label(label="General"))

        # page 2
        self.page2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.page2.set_border_width(10)
        self.notebook.append_page(self.page2, Gtk.Label(label="Settings"))

        # start page 1
        label = Gtk.Label(label="Hostname")
        label.set_xalign(0.0)
        self.page1.pack_start(label, False, False, 0)

        # self.hostname = Gtk.Entry()
        # self.hostname.set_text("host.example.org")
        # self.hostname.set_activates_default(True)
        # self.hostname.grab_focus()
        # self.page1.pack_start(self.hostname, False, False, 0)
        self.host_store = Gtk.ListStore(str)
        for row in self.config["hosts"]:
            self.host_store.append([row])
        # self.host_store.append(["host.example.org"])
        self.hostname = Gtk.ComboBox.new_with_model_and_entry(self.host_store)
        self.hostname.set_entry_text_column(0)
        self.hostname.set_active(0)
        child = self.hostname.get_child()
        child.set_activates_default(True)
        child.grab_focus()
        # renderer_text = Gtk.CellRendererText()
        # self.hostname.pack_start(renderer_text, True)
        # self.hostname.add_attribute(renderer_text, "text", 0)
        # self.hostname.connect("changed", self.on_combo_changed)

        self.page1.pack_start(self.hostname, False, False, 0)

        label = Gtk.Label(label="Username")
        label.set_xalign(0.0)
        self.page1.pack_start(label, False, False, 0)

        self.username = Gtk.Entry()
        self.username.set_text(self.config["username"])
        self.username.set_activates_default(True)
        self.page1.pack_start(self.username, False, False, 0)

        label = Gtk.Label(label="Password")
        label.set_xalign(0.0)
        self.page1.pack_start(label, False, False, 0)

        self.password = Gtk.Entry()
        self.password.set_text("")
        self.password.set_activates_default(True)
        self.password.set_visibility(False)
        self.page1.pack_start(self.password, False, False, 0)
        # end page 1

        # start page 2
        self.check_fullscreen = Gtk.CheckButton(label="Fullscreen")
        # self.check_fullscreen.connect("toggled", self.on_editable_toggled)
        self.check_fullscreen.set_active(self.config["fullscreen"])
        self.page2.pack_start(self.check_fullscreen, False, False, 0)

        self.check_clipboard = Gtk.CheckButton(label="Clipboard")
        # self.check_clipboard.connect("toggled", self.on_editable_toggled)
        self.check_clipboard.set_active(self.config["clipboard"])
        self.page2.pack_start(self.check_clipboard, False, False, 0)

        self.check_homedrive = Gtk.CheckButton(label="Home Drives")
        # self.check_editable.connect("toggled", self.on_editable_toggled)
        self.check_homedrive.set_active(self.config["homedrive"])
        self.page2.pack_start(self.check_homedrive, False, False, 0)

        # self.check_editable = Gtk.CheckButton(label="Editable")
        # self.check_editable.connect("toggled", self.on_editable_toggled)
        # self.check_editable.set_active(True)
        # self.page2.pack_start(self.check_editable, False, False, 0)
        # end page 2

        self.buttonbox = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.buttonbox.set_border_width(10)
        self.mainbox.pack_end(self.buttonbox, False, False, 0)

        button = Gtk.Button.new_with_mnemonic("_Connect")
        button.connect("clicked", self.on_ok_clicked)
        button.set_can_default(True)
        self.set_default(button)
        self.buttonbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Close")
        button.connect("clicked", self.on_close_clicked)
        self.buttonbox.pack_start(button, True, True, 0)

    def on_ok_clicked(self, button):
        print("on_ok_clicked")

        # update host list
        self.update_hosts()

        # the application
        args = ["xfreerdp"]

        # args.append("/d:domain")

        if self.hostname.get_child().get_text() == "":
            self.show_error("Hostname missing")
            return
        else:
            args.append("/v:{0}".format(self.hostname.get_child().get_text()))

        if self.username.get_text() == "":
            self.show_error("Username missing")
            return
        else:
            args.append("/u:{0}".format(self.username.get_text()))

        if self.password.get_text() == "":
            self.show_error("Password missing")
            return
        else:
            args.append("/p:{0}".format(self.password.get_text()))

        args.append("/disp")
        args.append("/dynamic-resolution")
        args.append("/rfx")
        args.append("/gfx")
        args.append("/gfx-progressive")
        args.append("/multitransport")
        args.append("/cert-ignore")
        args.append("/cert-tofu")
        args.append("/menu-anims")
        args.append("/fonts")
        args.append("/aero")
        args.append("/window-drag")
        args.append("/kbd:German")

        if self.check_fullscreen.get_active():
            args.append("/f")
        if self.check_clipboard.get_active():
            args.append("/clipboard")
        if self.check_homedrive.get_active():
            args.append("/home-drive")

        self.run_process(args)

    def on_close_clicked(self, button):
        print("on_close_clicked")
        self.close()
        # Gtk.main_quit()

    def on_delete_event(event, self, widget):
        print("on_delete_event")
        self.save_config()
        return False

    def show_error(self, text):
        dialog = Gtk.MessageDialog(
            transient_for=self, flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text="Error",)
        dialog.format_secondary_text(text)
        dialog.run()
        dialog.destroy()

    def run_process(self, args):
        print(args)
        proc = subprocess.Popen(args)
        # streamdata = proc.communicate()[0]
        # print(proc.returncode)

    def update_hosts(self):
        exists = False
        iter = None
        item = self.hostname.get_child().get_text()
        for row in self.host_store:
            print(row[0], item)
            if row[0] == item:
                exists = True
                iter = row.iter
        if not exists:
            self.host_store.prepend([item])
        else:
            self.host_store.move_after(iter, None)

    def load_config(self):
        cf = os.path.expanduser("~") + "/.freerdp-gui.json"
        print("config_path:", cf)
        config = {}
        try:
            with open(cf, "r") as file:
                config = json.load(file)
        except:
            pass

        self.config = {
            "hosts": config["hosts"] if "hosts" in config else [],
            "username": config["username"] if "username" in config else "",
            "fullscreen": config["fullscreen"] if "fullscreen" in config else False,
            "clipboard": config["clipboard"] if "clipboard" in config else True,
            "homedrive": config["homedrive"] if "homedrive" in config else True
        }
        print(json.dumps(self.config, indent=4))

    def save_config(self):
        hosts = []
        for row in self.host_store:
            hosts.append(row[0])

        config = {
            "hosts": hosts,
            "username": self.username.get_text(),
            "fullscreen": self.check_fullscreen.get_active(),
            "clipboard": self.check_clipboard.get_active(),
            "homedrive": self.check_homedrive.get_active()
        }

        print(json.dumps(config, indent=4))

        cf = os.path.expanduser("~") + "/.freerdp-gui.json"
        print("config_path:", cf)
        try:
            with open(cf, "w") as file:
                file.write(json.dumps(config, indent=4))
        except:
            pass


if __name__ == "__main__":
    window = EntryWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
