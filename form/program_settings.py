from os import getcwd
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from function import my_sql


class SettingsPath(QDialog):
    def __init__(self):
        super(SettingsPath, self).__init__()
        loadUi(getcwd() + '/ui/program_settings_path.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.set_info()

    def set_info(self):
        query = 'SELECT Name, program_settings_path.Values FROM program_settings_path'
        sql_ret = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_ret)):
            QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)
            return False

        for path in sql_ret:
            if path[0] == "Путь корень рабочие":
                self.le_work_path.setText(path[1])
            elif path[0] == "Путь корень клиенты":
                self.le_clients_path.setText(path[1])
            elif path[0] == "Путь корень бирки":
                self.le_article_label_path.setText(path[1])

    def work_path(self):
        self.le_work_path.setText(QFileDialog.getExistingDirectory(self))

    def clients_path(self):
        self.le_clients_path.setText(QFileDialog.getExistingDirectory(self))

    def article_label(self):
        self.le_article_label_path.setText(QFileDialog.getExistingDirectory(self))

    def ok(self):
        query = "UPDATE program_settings_path SET `Values` = %s WHERE Name = %s"
        parametrs = ((self.le_work_path.text(), "Путь корень рабочие"),
                     (self.le_clients_path.text(), "Путь корень клиенты"), (self.le_article_label_path.text(), "Путь корень бирки"))
        sql_ret = my_sql.sql_many(query, parametrs)
        if "mysql.connector.errors" in str(type(sql_ret)):
            QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)
            return False


class SettingsRoad(QDialog):
    def __init__(self):
        super(SettingsRoad, self).__init__()
        loadUi(getcwd() + '/ui/program_settings_road.ui', self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))
        self.set_info()

    def set_info(self):
        query = 'SELECT Id, One_year, Many_year FROM program_settings_road'
        sql_ret = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_ret)):
            QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)
            return False

        self.row_id = sql_ret[0][0]

        self.le_one_year.setText(str(sql_ret[0][1]))
        self.le_many_year.setText(str(sql_ret[0][2]))

    def ui_ok(self):
        query = 'UPDATE program_settings_road SET One_year = %s, Many_year = %s WHERE Id = %s'
        sql_ret = my_sql.sql_change(query, (self.le_one_year.text(), self.le_many_year.text(), self.row_id))
        if "mysql.connector.errors" in str(type(sql_ret)):
            QMessageBox.critical(self, "Ошибка sql", sql_ret.msg, QMessageBox.Ok)
            return False

        self.close()
        self.destroy()