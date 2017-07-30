# -*- coding: utf-8 -*-

import mainwindow
from PyQt5.QtWidgets import QMainWindow


class Frec(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = mainwindow.Ui_Frec()
        self.ui.setupUi(self)

        self.init_frec()

    def init_frec(self):
        self.ui.btn_register.clicked.connect(self.add_new_member)
        self.ui.btn_remove(self.delete_member)

        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_export.clicked(self.export_cvs)
        self.ui.btn_import(self.import_cvs)

    # Save new member to database
    def save_new_member(self):
        pass

    # Delete chosen member on tableView
    def delete_member(self):
        pass

    # Clear inside the line edits in registration form
    def clear_form(self):
        pass

    # Export members in the database as csv
    def export_cvs(self):
        pass

    # Import members from a csv file
    def import_cvs(self):
        pass
