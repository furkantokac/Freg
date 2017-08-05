# -*- coding: utf-8 -*-

import mainwindow, sys
from database import MongoDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

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

        self.ui.btn_connectDb.clicked.connect(self.connect_db)

        self.connect_db()
        self.show_member_at_tableWidget()

    def show_message(self, msg, timeout=3000):
        self.ui.statusBar.showMessage(msg, timeout)

    def connect_db(self):
        dbName = self.ui.lne_dbName.text()
        if self.db.connect(dbName):
            self.show_message("Database connection with '" + dbName + "' is successful.")
            self.ui.lbl_dbConnection.setText("Database : Connected '" + dbName + "'")
            self.ui.lbl_dbConnection.setStyleSheet('color: green')
        else:
            self.ui.lbl_dbConnection.setText("Database : Disconnected")
            self.ui.lbl_dbConnection.setStyleSheet('color: red')
            self.show_message("Database connection couldn't established!")
            return False

        return True

    # Save new member to database
    def save_new_member(self):
    #def clear_form(self):

        new = {
            "firstname": self.ui.lne_firstName.text(),
            "surname": self.ui.lne_lastName.text(),
            "department": self.ui.comboBox_department.currentText(),
            "email": self.ui.lne_email.text(),
            "mobilencc": self.ui.lne_mobileCyp.text(),
            "mobileother": self.ui.lne_mobileOther.text(),
        }

        self.db.add_new_member(new['firstname'], new['surname'], new['email'], new['department'], new['mobilencc'],
                               new['mobileother'])
        self.add_member_to_tableWidget(new['firstname'], new['surname'], new['email'], new['department'],
                                       new['mobilencc'], new['mobileother'])

    # show member on tableview
    def add_member_to_tableWidget(self, firstname, surname, email, department, mobilencc, mobileother):
        rowPoint = self.ui.tableWidget.rowCount()
        self.table.insertRow(rowPoint)
        self.table.setItem(rowPoint, 0, QTableWidgetItem(firstname))
        self.table.setItem(rowPoint, 1, QTableWidgetItem(surname))
        self.table.setItem(rowPoint, 2, QTableWidgetItem(email))
        self.table.setItem(rowPoint, 3, QTableWidgetItem(department))
        self.table.setItem(rowPoint, 4, QTableWidgetItem(mobilencc))
        self.table.setItem(rowPoint, 5, QTableWidgetItem(mobileother))

    def show_member_at_tableWidget(self):
        self.table = self.ui.tableWidget
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["firstname", "surname", "department", "email", "mobilencc", "mobileother"])
        quary = {}
        result = self.db.query_result_multi("Member", quary)
        for member in result:
            self.add_member_to_tableWidget(member["name"]["first"], member["name"]["last"], member["department"],
                                           member["email"], member["mobileNo"]["ncc"], member["mobileNo"]["other"])

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
        pass  # TODO

    # Import members from a csv file
    def import_cvs(self):
        pass  # TODO

    def create_desktop_entry(self):
        # TODO: Replace [-HOMEDIR-] inside ./data/freg.desktop and copy it to ~/.local/share/applications/
        pass


    def arrange_for_cvs(self):
        dbb = self.db.query_result_multi("Member",{})

        for member in dbb:
            one=member["name"]["first"]+","+member["name"]["last"]+","+member["email"]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Frec()

    myapp.show()
    sys.exit(app.exec_())