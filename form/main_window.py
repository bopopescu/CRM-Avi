from os import getcwd
from PyQt5.QtWidgets import QMainWindow, QMdiSubWindow, QLabel
from PyQt5.uic import loadUiType
from function import my_sql
from form import login_window, provider, comparing, staff, program_settings, notification, \
    clients, operation, other, audit, warehouse_material, warehouse_accessories
from form import article, order, cut, pay, salary, operation_list, warehouse_product, beika,\
    warehouse_rest, supply_material, supply_accessories, scan_pack, settings_access
from form import report_supply, report_cost_article, test_window, report_sibestoimost
from form import staff_traffic
from form import report_order
from classes.my_class import User
from PyQt5.QtGui import QIcon, QBrush, QImage
import sys

main_class = loadUiType(getcwd() + '/ui/main.ui')[0]


class MainWindow(QMainWindow, main_class):
    def __init__(self, *args):

        super(MainWindow, self).__init__(*args)
        self.setupUi(self)
        self.mdi.setBackground(QBrush(QImage(getcwd() + "/images/logo.png")))
        self.setWindowIcon(QIcon(getcwd() + "/images/icon.ico"))

        self.menu_3.setEnabled(False)
        self.ma_sibest.setEnabled(False)
        self.menu_14.setEnabled(False)

        self.show()
        self.setDisabled(True)

        self.login = login_window.LoginWindow(self)
        # self.admin_login()

    def access(self):
        for item in User().access_list(self.__class__.__name__):
            a = getattr(self, item["atr1"])
            if item["atr2"]:
                a = getattr(a, item["atr2"])

            if item["value"]:
                try:
                    val = int(item["value"])
                except:
                    val = item["value"]
                a(val)
            else:
                a()

    def view_material(self):
        self.material = supply_material.MaterialSupplyList()
        self.sub_material = QMdiSubWindow()
        self.sub_material.setWidget(self.material)
        self.mdi.addSubWindow(self.sub_material)
        self.sub_material.resize(self.material.size())
        self.sub_material.show()

    def view_material_provider(self):
        self.mat_prov = provider.ProviderMaterial()
        self.sub_provider = QMdiSubWindow()
        self.sub_provider.setWidget(self.mat_prov)
        self.mdi.addSubWindow(self.sub_provider)
        self.sub_provider.resize(self.mat_prov.size())
        self.sub_provider.show()

    def view_material_name(self):
        self.material_neme = supply_material.MaterialName()
        self.sub_mater_name = QMdiSubWindow()
        self.sub_mater_name.setWidget(self.material_neme)
        self.mdi.addSubWindow(self.sub_mater_name)
        self.sub_mater_name.resize(self.material_neme.size())
        self.sub_mater_name.show()

    def view_comparing_name(self):
        self.comparing_name = comparing.ComparingName()
        self.sub_comp_name = QMdiSubWindow()
        self.sub_comp_name.setWidget(self.comparing_name)
        self.mdi.addSubWindow(self.sub_comp_name)
        self.sub_comp_name.resize(self.comparing_name.size())
        self.sub_comp_name.show()

    def view_accessories_name(self):
        self.accessories_name = supply_accessories.AccessoriesName()
        self.sub_accsess_name = QMdiSubWindow()
        self.sub_accsess_name.setWidget(self.accessories_name)
        self.mdi.addSubWindow(self.sub_accsess_name)
        self.sub_accsess_name.resize(self.accessories_name.size())
        self.sub_accsess_name.show()

    def view_accessories_provider(self):
        self.access_prov = provider.ProviderAccessories()
        self.sub_provider_access = QMdiSubWindow()
        self.sub_provider_access.setWidget(self.access_prov)
        self.mdi.addSubWindow(self.sub_provider_access)
        self.sub_provider_access.resize(self.access_prov.size())
        self.sub_provider_access.show()

    def view_accessories(self):
        self.accessories = supply_accessories.AccessoriesSupplyList()
        self.accessories.set_settings()
        self.sub_accessories = QMdiSubWindow()
        self.sub_accessories.setWidget(self.accessories)
        self.mdi.addSubWindow(self.sub_accessories)
        self.sub_accessories.resize(self.accessories.size())
        self.sub_accessories.show()

    def view_staff_country(self):
        self.staff_country = staff.Country()
        self.sub_staff_country = QMdiSubWindow()
        self.sub_staff_country.setWidget(self.staff_country)
        self.mdi.addSubWindow(self.sub_staff_country)
        self.sub_staff_country.resize(self.staff_country.size())
        self.sub_staff_country.show()

    def view_staff_position(self):
        self.staff_position = staff.StaffPosition()
        self.sub_staff_position = QMdiSubWindow()
        self.sub_staff_position.setWidget(self.staff_position)
        self.mdi.addSubWindow(self.sub_staff_position)
        self.sub_staff_position.resize(self.staff_position.size())
        self.sub_staff_position.show()

    def view_staff_list(self):
        self.staff_list = staff.Staff()
        self.sub_staff_list = QMdiSubWindow()
        self.sub_staff_list.setWidget(self.staff_list)
        self.mdi.addSubWindow(self.sub_staff_list)
        self.sub_staff_list.resize(self.staff_list.size())
        self.sub_staff_list.show()

    def view_staff_calendar(self):
        self.staff_calendar = notification.WorkCalendar()
        self.sub_staff_calendar = QMdiSubWindow()
        self.sub_staff_calendar.setWidget(self.staff_calendar)
        self.mdi.addSubWindow(self.sub_staff_calendar)
        self.sub_staff_calendar.resize(self.staff_calendar.size())
        self.sub_staff_calendar.show()

    def view_staff_card(self):
        self.staff_card = staff_traffic.StaffCardList()
        self.sub_staff_card = QMdiSubWindow()
        self.sub_staff_card.setWidget(self.staff_card)
        self.mdi.addSubWindow(self.sub_staff_card)
        self.sub_staff_card.resize(self.staff_card.size())
        self.sub_staff_card.show()

    def view_staff_traffic(self):
        self.staff_traffic = staff_traffic.StaffTraffic()
        self.sub_staff_traffic = QMdiSubWindow()
        self.sub_staff_traffic.setWidget(self.staff_traffic)
        self.mdi.addSubWindow(self.sub_staff_traffic)
        self.sub_staff_traffic.resize(self.staff_traffic.size())
        self.sub_staff_traffic.show()

    def view_settings_path(self):
        self.sett_path = program_settings.SettingsPath()
        self.sub_sett_path = QMdiSubWindow()
        self.sub_sett_path.setWidget(self.sett_path)
        self.mdi.addSubWindow(self.sub_sett_path)
        self.sub_sett_path.resize(self.sett_path.size())
        self.sub_sett_path.show()

    def view_settings_road(self):
        self.sett_road = program_settings.SettingsRoad()
        self.sub_sett_road = QMdiSubWindow()
        self.sub_sett_road.setWidget(self.sett_road)
        self.mdi.addSubWindow(self.sub_sett_road)
        self.sub_sett_road.resize(self.sett_road.size())
        self.sub_sett_road.show()

    def view_clients(self):
        self.clients = clients.ClientList()
        self.sub_clients = QMdiSubWindow()
        self.sub_clients.setWidget(self.clients)
        self.mdi.addSubWindow(self.sub_clients)
        self.sub_clients.resize(self.clients.size())
        self.sub_clients.show()

    def view_operation(self):
        self.operation_list = operation.OperationList()
        self.sub_operation_list = QMdiSubWindow()
        self.sub_operation_list.setWidget(self.operation_list)
        self.mdi.addSubWindow(self.sub_operation_list)
        self.sub_operation_list.resize(self.operation_list.size())
        self.sub_operation_list.show()

    def view_product(self):
        self.article_list = article.ArticleList()
        self.sub_article_list = QMdiSubWindow()
        self.sub_article_list.setWidget(self.article_list)
        self.mdi.addSubWindow(self.sub_article_list)
        self.sub_article_list.resize(self.article_list.size())
        self.sub_article_list.show()

    def view_order_list(self):
        self.order_list = order.OrderList()
        self.sub_order_list = QMdiSubWindow()
        self.sub_order_list.setWidget(self.order_list)
        self.mdi.addSubWindow(self.sub_order_list)
        self.sub_order_list.resize(self.order_list.size())
        self.sub_order_list.show()

    def view_cut_mission_list(self):
        self.cut_mission_list = cut.CutListMission()
        self.sub_cut_mission_list = QMdiSubWindow()
        self.sub_cut_mission_list.setWidget(self.cut_mission_list)
        self.mdi.addSubWindow(self.sub_cut_mission_list)
        self.sub_cut_mission_list.resize(self.cut_mission_list.size())
        self.sub_cut_mission_list.show()

    def view_cut_list(self):
        self.cut_list = cut.CutList()
        self.sub_cut_list = QMdiSubWindow()
        self.sub_cut_list.setWidget(self.cut_list)
        self.mdi.addSubWindow(self.sub_cut_list)
        self.sub_cut_list.resize(self.cut_list.size())
        self.sub_cut_list.show()

    def view_pay_plus_minus(self):
        self.pay_plus_minus = pay.PayList()
        self.sub_pay_plus_minus = QMdiSubWindow()
        self.sub_pay_plus_minus.setWidget(self.pay_plus_minus)
        self.mdi.addSubWindow(self.sub_pay_plus_minus)
        self.sub_pay_plus_minus.resize(self.pay_plus_minus.size())
        self.sub_pay_plus_minus.show()

    def view_other_order_edi(self):
        self.input_order_edi = other.OrderEDI()
        self.sub_input_order_edi = QMdiSubWindow()
        self.sub_input_order_edi.setWidget(self.input_order_edi)
        self.mdi.addSubWindow(self.sub_input_order_edi)
        self.sub_input_order_edi.resize(self.input_order_edi.size())
        self.sub_input_order_edi.show()

    def view_audit_verification(self):
        self.audit_verification = audit.AuditVerification()
        self.sub_audit_verification = QMdiSubWindow()
        self.sub_audit_verification.setWidget(self.audit_verification)
        self.mdi.addSubWindow(self.sub_audit_verification)
        self.sub_audit_verification.resize(self.audit_verification.size())
        self.sub_audit_verification.show()

    def view_salary_work(self):
        self.salary_list = salary.SalaryList()
        self.sub_salary_list = QMdiSubWindow()
        self.sub_salary_list.setWidget(self.salary_list)
        self.mdi.addSubWindow(self.sub_salary_list)
        self.sub_salary_list.resize(self.salary_list.size())
        self.sub_salary_list.show()

    def view_pack_operation_list(self):
        self.operation_list = operation_list.PayList()
        self.sub_operation_list = QMdiSubWindow()
        self.sub_operation_list.setWidget(self.operation_list)
        self.mdi.addSubWindow(self.sub_operation_list)
        self.sub_operation_list.resize(self.operation_list.size())
        self.sub_operation_list.show()

    def view_product_warehouse(self):
        self.product_warehouse = warehouse_product.Warehouse()
        self.sub_product_warehouse = QMdiSubWindow()
        self.sub_product_warehouse.setWidget(self.product_warehouse)
        self.mdi.addSubWindow(self.sub_product_warehouse)
        self.sub_product_warehouse.resize(self.product_warehouse.size())
        self.sub_product_warehouse.show()

    def view_warehouse_rest(self):
        self.rest_warehouse = warehouse_rest.WarehouseRest()
        self.sub_rest_warehouse = QMdiSubWindow()
        self.sub_rest_warehouse.setWidget(self.rest_warehouse)
        self.mdi.addSubWindow(self.sub_rest_warehouse)
        self.sub_rest_warehouse.resize(self.rest_warehouse.size())
        self.sub_rest_warehouse.show()

    def view_warehouse_material(self):
        self.material_warehouse = warehouse_material.Warehouse()
        self.sub_material_warehouse = QMdiSubWindow()
        self.sub_material_warehouse.setWidget(self.material_warehouse)
        self.mdi.addSubWindow(self.sub_material_warehouse)
        self.sub_material_warehouse.resize(self.material_warehouse.size())
        self.sub_material_warehouse.show()

    def view_warehouse_accessories(self):
        self.accessories_warehouse = warehouse_accessories.Warehouse()
        self.sub_material_accessories = QMdiSubWindow()
        self.sub_material_accessories.setWidget(self.accessories_warehouse)
        self.mdi.addSubWindow(self.sub_material_accessories)
        self.sub_material_accessories.resize(self.accessories_warehouse.size())
        self.sub_material_accessories.show()

    def view_beika(self):
        self.beika = beika.BeikaList()
        self.sub_beika = QMdiSubWindow()
        self.sub_beika.setWidget(self.beika)
        self.mdi.addSubWindow(self.sub_beika)
        self.sub_beika.resize(self.beika.size())
        self.sub_beika.show()

    def view_supply_material(self):
        self.supply_material = supply_material.MaterialSupplyList()
        self.sub_supply_material = QMdiSubWindow()
        self.sub_supply_material.setWidget(self.supply_material)
        self.mdi.addSubWindow(self.sub_supply_material)
        self.sub_supply_material.resize(self.supply_material.size())
        self.sub_supply_material.show()

    def view_supply_accessories(self):
        self.supply_accessories = supply_accessories.AccessoriesSupplyList()
        self.sub_supply_accessories = QMdiSubWindow()
        self.sub_supply_accessories.setWidget(self.supply_accessories)
        self.mdi.addSubWindow(self.sub_supply_accessories)
        self.sub_supply_accessories.resize(self.supply_accessories.size())
        self.sub_supply_accessories.show()

    def view_scan_pack(self):
        self.scan_pack = scan_pack.ScanPack()
        self.sub_scan_pack = QMdiSubWindow()
        self.sub_scan_pack.setWidget(self.scan_pack)
        self.mdi.addSubWindow(self.sub_scan_pack)
        self.sub_scan_pack.resize(self.scan_pack.size())
        self.sub_scan_pack.show()

    def view_settings_access(self):
        self.settings_access = settings_access.Access()
        self.sub_settings_access = QMdiSubWindow()
        self.sub_settings_access.setWidget(self.settings_access)
        self.mdi.addSubWindow(self.sub_settings_access)
        self.sub_settings_access.resize(self.settings_access.size())
        self.sub_settings_access.show()

    def view_report_need_article_order(self):
        self.report_need_article = report_order.NeedArticleOrder()
        self.sub_report_need_article = QMdiSubWindow()
        self.sub_report_need_article.setWidget(self.report_need_article)
        self.mdi.addSubWindow(self.sub_report_need_article)
        self.sub_report_need_article.resize(self.report_need_article.size())
        self.sub_report_need_article.show()

    def view_report_supply(self):
        self.report_supply = report_supply.ReportSupply()
        self.sub_report_supply = QMdiSubWindow()
        self.sub_report_supply.setWidget(self.report_supply)
        self.mdi.addSubWindow(self.sub_report_supply)
        self.sub_report_supply.resize(self.report_supply.size())
        self.sub_report_supply.show()

    def view_report_cost_article(self):
        self.report_cost_article = report_cost_article.ReportCostArticle()
        self.sub_report_cost_article = QMdiSubWindow()
        self.sub_report_cost_article.setWidget(self.report_cost_article)
        self.mdi.addSubWindow(self.sub_report_cost_article)
        self.sub_report_cost_article.resize(self.report_cost_article.size())
        self.sub_report_cost_article.show()

    def view_report_sibestoimost(self):
        self.report_sibest = report_sibestoimost.ReportSibestoimost()
        self.sub_report_sibest = QMdiSubWindow()
        self.sub_report_sibest.setWidget(self.report_sibest)
        self.mdi.addSubWindow(self.sub_report_sibest)
        self.sub_report_sibest.resize(self.report_sibest.size())
        self.sub_report_sibest.show()

    def view_test_window(self):
        self.test_window = test_window.TestWindow()
        self.sub_test_window = QMdiSubWindow()
        self.sub_test_window.setWidget(self.test_window)
        self.mdi.addSubWindow(self.sub_test_window)
        self.sub_test_window.resize(self.test_window.size())
        self.sub_test_window.show()

    def login_access(self):
        self.statusBar().showMessage("Вы вошли как -= %s =-" % User().position_name())
        self.setEnabled(True)
        self.setFocus()
        self.access()

    def admin_login(self):
        self.statusBar().showMessage("Вы вошли как -= %s =-" % User().position_name())
        self.setEnabled(True)
        self.setFocus()
        self.access()

    def beika_no_finished(self):
        query = """SELECT COUNT(*) FROM beika WHERE Finished = 0"""
        sql_info = my_sql.sql_select(query)
        if "mysql.connector.errors" in str(type(sql_info)):
            beika_txt = "error sql"
        else:
            beika_txt = "Не зкарыто бейки: " + str(sql_info[0][0])
        beika = QLabel(beika_txt)
        self.statusBar().addPermanentWidget(beika)

    def closeEvent(self, e):
        e.accept()
        sys.exit()
