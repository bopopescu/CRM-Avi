from os import getcwd
import re
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMessageBox, QMainWindow,  QTableWidgetItem, QProgressDialog, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, QDate, QCoreApplication
from function import my_sql
from classes import cut, print_qt
from decimal import Decimal
from function import table_to_html, to_excel

material_consumption_class = loadUiType(getcwd() + '/ui/report_material_consumption.ui')[0]


class ReportMaterialConsumption(QMainWindow, material_consumption_class):
    def __init__(self):
        super(ReportMaterialConsumption, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.start_settings()

    def start_settings(self):
        self.de_material_from.setDate(QDate.currentDate().addMonths(-1))
        self.de_material_to.setDate(QDate.currentDate())

        self.tw_material.horizontalHeader().resizeSection(0, 150)
        self.tw_material.horizontalHeader().resizeSection(1, 70)
        self.tw_material.horizontalHeader().resizeSection(2, 80)
        self.tw_material.horizontalHeader().resizeSection(3, 70)
        self.tw_material.horizontalHeader().resizeSection(4, 80)

        self.tw_material_info.horizontalHeader().resizeSection(0, 90)
        self.tw_material_info.horizontalHeader().resizeSection(1, 80)
        self.tw_material_info.horizontalHeader().resizeSection(2, 80)

    def ui_calc_material(self):
        # Расчет общего расхода ткани
        query = """SELECT material_name.Id, material_name.Name, SUM(material_supplyposition.Weight),
                        SUM(material_supplyposition.Weight * material_supplyposition.Price)
                      FROM material_supply LEFT JOIN material_supplyposition ON material_supply.Id = material_supplyposition.Material_SupplyId
                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                      WHERE material_supply.Data >= %s AND material_supply.Data <= %s
                      GROUP BY material_name.Id"""
        sql_material_in = my_sql.sql_select(query, (self.de_material_from.date().toString(Qt.ISODate), self.de_material_to.date().toString(Qt.ISODate)))
        if "mysql.connector.errors" in str(type(sql_material_in)):
            QMessageBox.critical(self, "Ошибка sql получения приходов ткани", sql_material_in.msg, QMessageBox.Ok)
            return False

        query = """SELECT material_name.Id, material_name.Name, SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                      LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                        LEFT JOIN material_supply ON material_supplyposition.Material_SupplyId = material_supply.Id
                        LEFT JOIN material_name ON material_supplyposition.Material_NameId = material_name.Id
                      WHERE transaction_records_material.Note NOT LIKE 'Заказ %'
                        AND transaction_records_material.Date >= %s AND transaction_records_material.Date <= %s
                      GROUP BY material_name.Id"""
        sql_material_out = my_sql.sql_select(query, (self.de_material_from.date().toString(Qt.ISODate), self.de_material_to.date().toString(Qt.ISODate)))
        if "mysql.connector.errors" in str(type(sql_material_out)):
            QMessageBox.critical(self, "Ошибка sql получения расходов ткани", sql_material_out.msg, QMessageBox.Ok)
            return False

        all_list_consumption = []
        for out in sql_material_out:
            fillst = list(filter(lambda s: s[0] == out[0], sql_material_in))

            if fillst:
                newlst = [out[0], out[1], fillst[0][2], fillst[0][3], out[2], out[3]]
            else:
                newlst = [out[0], out[1], 0, 0, out[2], out[3]]

            all_list_consumption.append(newlst)

        self.tw_material.clearContents()
        self.tw_material.setRowCount(0)

        all_weight_in = 0
        all_weight_out = 0
        all_sum_in = 0
        all_sum_out = 0

        for i in all_list_consumption:
            self.tw_material.insertRow(self.tw_material.rowCount())

            item = QTableWidgetItem(str(i[1]))
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 0, item)

            all_weight_in += i[2]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[2], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 1, item)

            all_sum_in += i[3]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[3], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 2, item)

            all_weight_out += i[4]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[4], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 3, item)

            all_sum_out += i[5]
            text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(i[5], 2)))
            item = QTableWidgetItem(text)
            item.setData(5, i[0])
            self.tw_material.setItem(self.tw_material.rowCount() - 1, 4, item)

        self.tw_material.insertRow(self.tw_material.rowCount())

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_weight_in, 2)))
        item = QTableWidgetItem(text)
        self.tw_material.setItem(self.tw_material.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_in, 2)))
        item = QTableWidgetItem(text)
        self.tw_material.setItem(self.tw_material.rowCount() - 1, 2, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_weight_out, 2)))
        item = QTableWidgetItem(text)
        self.tw_material.setItem(self.tw_material.rowCount() - 1, 3, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(all_sum_out, 2)))
        item = QTableWidgetItem(text)
        self.tw_material.setItem(self.tw_material.rowCount() - 1, 4, item)

    def ui_calc_material_info(self):
        # Расчет подробный
        self.tw_material_info.clearContents()
        self.tw_material_info.setRowCount(0)

        filter_date = (self.de_material_from.date().toString(Qt.ISODate), self.de_material_to.date().toString(Qt.ISODate))

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%пачк%'
                        AND transaction_records_material.Date >= %s AND transaction_records_material.Date <= %s"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на пачки", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Пачки")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%обрез%'
                        AND transaction_records_material.Date >= %s AND transaction_records_material.Date <= %s"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на обрезь", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Обрезь")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%доп.%'
                        AND transaction_records_material.Date >= %s AND transaction_records_material.Date <= %s"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на доп ткань", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Доп. ткань")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%бейк%'
                        AND transaction_records_material.Date >= %s AND transaction_records_material.Date <= %s"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на бйеку", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Бейка")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)

        query = """SELECT SUM(transaction_records_material.Balance),
                        SUM(transaction_records_material.Balance * material_supplyposition.Price)
                      FROM transaction_records_material
                        LEFT JOIN material_balance ON transaction_records_material.Supply_Balance_Id = material_balance.Id
                        LEFT JOIN material_supplyposition ON material_balance.Material_SupplyPositionId = material_supplyposition.Id
                      WHERE Note LIKE '%продаж%'
                        AND transaction_records_material.Date >= %s AND transaction_records_material.Date <= %s"""
        sql_info = my_sql.sql_select(query, filter_date)[0]
        if "mysql.connector.errors" in str(type(sql_info)):
            QMessageBox.critical(self, "Ошибка sql получения расхода на продажу ткани", sql_info.msg, QMessageBox.Ok)
            return False

        self.tw_material_info.insertRow(self.tw_material_info.rowCount())

        item = QTableWidgetItem("Продажа ткани")
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 0, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[0], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 1, item)

        text = re.sub(r'(?<=\d)(?=(\d\d\d)+\b.)', ' ', str(round(sql_info[1], 2)))
        item = QTableWidgetItem(text)
        self.tw_material_info.setItem(self.tw_material_info.rowCount() - 1, 2, item)