# -*- coding: utf-8 -*-
from PyQt5.QtCore import QModelIndex

import mainwindow, sys, config
from database import MongoDatabase
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtGui import QIcon

__version__ = "0.0"


class Frec(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = mainwindow.Ui_Frec()
        self.ui.setupUi(self)
        self.db = MongoDatabase()

        self.init_frec()
        self.is_local_save = False

        self.dirs = config.Dirs()

        self.setWindowIcon(QIcon(self.dirs.appicon))

    def init_frec(self):
        self.ui.btn_register.clicked.connect(self.save_new_member)
        self.ui.btn_delete.clicked.connect(self.delete_member)
        self.ui.btn_createDesktopEntry.clicked.connect(self.create_desktop_entry)
        self.ui.btn_clear.clicked.connect(self.clear_form)
        self.ui.btn_export.clicked.connect(self.export_cvs)
        self.ui.btn_import.clicked.connect(self.import_cvs)
        self.ui.btn_exportAsCVS.clicked.connect(self.export_cvs)
        self.ui.checkBox_saveLocal.stateChanged.connect(self.save_local)

        self.ui.btn_connectDb.clicked.connect(self.connect_db)

        self.connect_db()
        self.show_member_at_tableWidget()

    def local_save_mode(self):
        return True

    def save_local(self, state):

        if state:
            self.is_local_save = True
        else:
            self.is_local_save = False

        return state

    def show_message(self, msg, timeout=3000):
        self.ui.statusBar.showMessage(msg, timeout)

    def connect_db(self):
        dbName = self.ui.lne_dbName.text()
        if self.db.connect(dbName):
            self.successful_db_connection(dbName)
        else:
            self.unsuccessful_db_connection()
            return False

        return True

    def successful_db_connection(self, dbName):
        self.show_message("Database connection with '" + dbName + "' is successful.")
        self.ui.lbl_dbConnection.setText("Database : Connected '" + dbName + "'")
        self.ui.lbl_dbConnection.setStyleSheet('color: green')

    def unsuccessful_db_connection(self):
        self.ui.lbl_dbConnection.setText("Database : Disconnected")
        self.ui.lbl_dbConnection.setStyleSheet('color: red')
        self.show_message("Database connection couldn't established!")

    # Save new member to database
    def save_new_member(self):
        new = {
            "firstname": self.ui.lne_firstName.text(),
            "surname": self.ui.lne_lastName.text(),
            "department": self.ui.comboBox_department.currentText(),
            "email": self.ui.lne_email.text(),
            "mobilecyp": self.ui.lne_mobileCyp.text(),
            "mobileother": self.ui.lne_mobileOther.text(),
        }

        if self.db.add_new_member(new['firstname'], new['surname'], new['email'], new['department'], new['mobilecyp'],
                                  new['mobileother']) is False:
            return False

        self.add_member_to_tableWidget(new['firstname'], new['surname'], new['email'], new['department'],
                                       new['mobilecyp'], new['mobileother'])

        self.show_message("New member is added to database.")

    # show member on tableview
    def add_member_to_tableWidget(self, firstname, surname, email, department, mobilecyp, mobileother):
        rowPoint = self.ui.tableWidget.rowCount()
        table = self.ui.tableWidget
        table.insertRow(rowPoint)
        table.setItem(rowPoint, 0, QTableWidgetItem(firstname))
        table.setItem(rowPoint, 1, QTableWidgetItem(surname))
        table.setItem(rowPoint, 2, QTableWidgetItem(email))
        table.setItem(rowPoint, 3, QTableWidgetItem(department))
        table.setItem(rowPoint, 4, QTableWidgetItem(mobilecyp))
        table.setItem(rowPoint, 5, QTableWidgetItem(mobileother))

    def show_member_at_tableWidget(self):
        table = self.ui.tableWidget
        table.setRowCount(0)
        # table.setColumnCount(6)
        # table.setHorizontalHeaderLabels(
        #    ["Name", "Surname", "E-mail", "Department", "Mobile No Cyp", "Mobile No Other"])
        query = {}  # means no condition. so it will get everyone.
        result = self.db.query_result_multi("Member", query)
        if not result:
            return False
        for member in result:
            self.add_member_to_tableWidget(member["name"]["first"], member["name"]["last"], member["email"]["other"],
                                           member["department"]["name"], member["mobileNo"]["cyp"],
                                           member["mobileNo"]["other"])

    # Delete chosen member on tableView
    def delete_member(self):
        indexes = self.ui.tableWidget.selectedIndexes()
        for i in indexes:
            # Following line get the selected row's email address
            email_to_delete = str(self.ui.tableWidget.item(i.row(), 2).text())

            # Delete member who has the email
            self.db.delete_member_by_email(email_to_delete)

        self.show_member_at_tableWidget()

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
        import csv
        with open("freg_export.cvs", "w") as file:
            csv_file = csv.writer(file)
            data = [self.ui.lne_firstName.text(), self.ui.lne_lastName.text()]
            csv_file.writerow(data)

    # Import members from a csv file
    def import_cvs(self):
        pass  # TODO

    def create_desktop_entry(self):
        if config.PLATFORM == "LINUX":
            with open(self.dirs.home + "/.local/share/applications/freg.desktop", "w") as fd:
                fd.write("[Desktop Entry]\n")
                fd.write("Version=1.0 \n")
                fd.write("Type=Application\n")
                fd.write("Name=Freg\n")
                fd.write("Exec=python3 " + self.dirs.app + "\n")
                fd.write("Icon=" + self.dirs.appicon + "\n")
                fd.write("Comment=Small member registration system\n")
                fd.write("Terminal=false\n")
            return

    def arrange_for_cvs(self):
        dbb = self.db.query_result_multi("Member", {})
        arranged_str = ""

        for member in dbb:
            one = member["name"]["first"] + "," + member["name"]["last"] + "," + member["email"]
            arranged_str += one + "\n"

        return arranged_str


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = Frec()

    myapp.show()
    sys.exit(app.exec_())
