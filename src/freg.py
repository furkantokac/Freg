# -*- coding: utf-8 -*-

import mainwindow, sys, csv
from database import MongoDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication



__version__ = "0.0"


class Frec(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = mainwindow.Ui_Frec()
        self.ui.setupUi(self)

        self.db = MongoDatabase()

        self.init_frec()

    def init_frec(self):
        self.ui.btn_register.clicked.connect(self.save_new_member)
        self.ui.btn_delete.clicked.connect(self.delete_member)

        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_export.clicked.connect(self.export_cvs)
        self.ui.btn_import.clicked.connect(self.import_cvs)
        self.ui.btn_exportAsCVS.clicked.connect(self.export_cvs)

        self.ui.btn_connectDb.clicked.connect(self.connect_db)

        self.connect_db()

    def show_message(self, msg, timeout=3000):
        self.ui.statusBar.showMessage(msg, timeout)

    def connect_db(self):
        dbName = self.ui.lne_dbName.text()
        if self.db.connect( dbName ):
            self.show_message("Database connection with '"+dbName+"' is successful.")
            self.ui.lbl_dbConnection.setText("Database : Connected '"+dbName+"'")
            self.ui.lbl_dbConnection.setStyleSheet('color: green')
        else:
            self.ui.lbl_dbConnection.setText("Database : Disconnected")
            self.ui.lbl_dbConnection.setStyleSheet('color: red')
            self.show_message("Database connection couldn't established!")
            return False

        return True

    # Save new member to database
    def save_new_member(self):

        new={
            "firstname":    self.ui.lne_firstName.text(),
            "surname":      self.ui.lne_lastName.text(),
            "department":   self.ui.comboBox_department.currentText(),
            "email":        self.ui.lne_email.text(),
            "mobilencc":    self.ui.lne_mobileCyp.text(),
            "mobileother":  self.ui.lne_mobileOther.text(),
        }

        self.db.add_new_member(new['firstname'],new['surname'],new['department'],new['email'],new['mobilencc'],new['mobileother'])

    # Delete chosen member on tableView
    def delete_member(self):
        pass  # TODO

    # Clear inside the line edits in registration form
    def clear_form(self):
        self.ui.lne_email.setText("")
        self.ui.lne_firstName.setText("")
        self.ui.lne_lastName.setText("")
        self.ui.lne_mobileCyp.setText("")
        self.ui.lne_mobileOther.setText("")
        self.ui.comboBox_department.setCurrentIndex(0)

    # Export members in the database as csv
    def export_cvs(self):

        try:
            file = open("freg_export.cvs","w+")
            csv_file = csv.writer(file)
            data = [self.ui.lne_firstName.text(), self.ui.lne_lastName.text()]
            csv_file.writerow(data)

        finally:
            file.close()


    # Import members from a csv file
    def import_cvs(self):
        pass  # TODO

    def create_desktop_entry(self):
        # TODO: Replace [-HOMEDIR-] inside ./data/freg.desktop and copy it to ~/.local/share/applications/
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Frec()

    myapp.show()
    sys.exit(app.exec_())
