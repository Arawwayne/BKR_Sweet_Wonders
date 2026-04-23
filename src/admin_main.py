import sys
import re
import csv
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QFrame, QDialog, QGridLayout, QComboBox, QMessageBox,
    QDialogButtonBox, QGroupBox, QStackedWidget, QSpinBox, QDoubleSpinBox,
    QCheckBox, QPlainTextEdit
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from crud import *

session_employee_id = None
session_access = None

roles = {
    1: 'Администратор',
    2: 'Менеджер'
}

#СТРАНИЦА АВТОРИЗАЦИИ

class LoginScreen(QMainWindow):
    #Сигнал для перехода к основному приложению после авторизации
    login_successful = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель администратора")
        self.setMinimumSize(1200, 600)

        #Устанавливаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #Основной layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(400, 40, 400, 100)
        main_layout.setSpacing(10)

        #Заголовок
        self.create_title(main_layout)

        #Форма авторизации
        self.create_login_form(main_layout)

        #Кнопка входа
        self.create_login_button(main_layout)

    def create_title(self, layout):
        title = QLabel("Вход в систему")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 35px;
                font-weight: bold;
                color: #0078d7;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title)

    def create_login_form(self, layout):
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)

        #Поле логина
        login_label = QLabel("Логин сотрудника")
        login_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333;
                margin: 0px;
            }
        """)
        form_layout.addWidget(login_label)

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин")
        self.login_input.setFixedHeight(35)
        self.login_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 14px;
                background-color: white;
                margin: 0px;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
        """)
        form_layout.addWidget(self.login_input)

        #Поле пароля
        password_label = QLabel("Пароль сотрудника")
        password_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #333;
                margin: 0px;
            }
        """)
        form_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(35)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 14px;
                background-color: white;
                margin: 0px;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
        """)
        form_layout.addWidget(self.password_input)

        layout.addWidget(form_widget)

    def create_login_button(self, layout):
        self.login_button = QPushButton("Авторизоваться")
        self.login_button.setFixedHeight(40)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004080;
            }
        """)
        self.login_button.clicked.connect(self.authenticate)

        self.login_input.returnPressed.connect(self.authenticate)
        self.password_input.returnPressed.connect(self.authenticate)

        layout.addWidget(self.login_button)

    def authenticate(self):
        login = self.login_input.text().strip()
        password = self.password_input.text()
        login_data = {
            "username": login,
            "password": password
        }

        if login == "":
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            self.login_input.setFocus()
            return

        if password == "":
            QMessageBox.warning(self, "Ошибка", "Введите пароль")
            self.password_input.setFocus()
            return
            
        try:
            response = post_employee_auth(login_data)
            global session_employee_id, session_access
            session_employee_id = response["employee_id"]
            session_access = get_employee(session_employee_id)["employee"]['position_id']
            self.login_successful.emit()
            self.close()
        except:
            QMessageBox.critical(
                self,
                "Ошибка",
                "Неверный логин или пароль."
            )
            self.password_input.clear()
            self.password_input.setFocus()      


#ОСНОВНОЕ ПРИЛОЖЕНИЕ

class OrderDetailDialog(QDialog):
    status_changed = Signal(str)

    def __init__(self, order_data, parent=None):
        super().__init__(parent)
        self.order_data = order_data
        self.id = order_data['id']
        self.setWindowTitle(f"Заказ: {order_data['id']}")
        self.setMinimumSize(600, 500)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLabel[heading="true"] {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-top: 10px;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        #Заголовок с номером заказа
        title_label = QLabel(f"Заказ: {self.order_data['id']}")
        title_label.setProperty("heading", True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title_label)

        #Информационная сетка
        info_group = QGroupBox("Информация о заказе")
        info_layout = QGridLayout(info_group)
        info_layout.setVerticalSpacing(10)
        info_layout.setHorizontalSpacing(20)

        row = 0
        self.userid = QLabel(str(self.order_data['user_id']))
        info_layout.addWidget(QLabel("ID пользователя:"), row, 0)
        info_layout.addWidget(self.userid, row, 1)

        row += 1
        self.phone = QLabel(self.order_data['phone'])
        info_layout.addWidget(QLabel("Телефон пользователя:"), row, 0)
        info_layout.addWidget(self.phone, row, 1)

        row += 1
        info_layout.addWidget(QLabel("Дата создания заказа:"), row, 0)
        self.created = QLabel(self.order_data['created_at'])
        info_layout.addWidget(self.created, row, 1)

        row += 1
        info_layout.addWidget(QLabel("Дата выполнения:"), row, 0)
        self.complete = QLabel(self.order_data['order_datetime'])
        info_layout.addWidget(self.complete, row, 1)

        row = 0
        info_layout.addWidget(QLabel("Наименование заведения:"), row, 2)
        self.branch = QLabel(self.order_data['branch_name'])
        info_layout.addWidget(self.branch, row, 3)

        row += 1
        info_layout.addWidget(QLabel("Адрес заведения:"), row, 2)
        self.branch_adress = QLabel(self.order_data['branch_address'])
        info_layout.addWidget(self.branch_adress, row, 3)

        info_layout.setColumnStretch(1, 1)
        info_layout.setColumnStretch(3, 1)

        layout.addWidget(info_group)

        #Таблица с изделиями
        items_group = QGroupBox("Состав заказа")
        items_layout = QVBoxLayout(items_group)

        self.items_table = QTableWidget()
        self.items_table.setColumnCount(3)
        self.items_table.setHorizontalHeaderLabels(["Изделие", "Кол-во", "Итого"])
        self.items_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.items_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.items_table.verticalHeader().setVisible(False)
        self.items_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.items_table.setAlternatingRowColors(True)

        self.populate_items_table()

        items_layout.addWidget(self.items_table)
        layout.addWidget(items_group)

        #Комментарий
        comm_group = QGroupBox("Комментарий к заказу")
        comm_layout = QVBoxLayout(comm_group)

        self.comm_text = QPlainTextEdit()
        self.comm_text.setPlainText(self.order_data['order_comment'])
        self.comm_text.setReadOnly(True)
        comm_layout.addWidget(self.comm_text)
        layout.addWidget(comm_group)

        #Сумма заказа
        total_frame = QFrame()
        total_frame.setFrameShape(QFrame.StyledPanel)
        total_frame.setStyleSheet("background-color: #f8f9fa; padding: 10px; border-radius: 5px;")
        total_layout = QHBoxLayout(total_frame)

        total_label = QLabel("Сумма заказа:")
        total_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.total_value = QLabel(str(self.order_data['total_ammount']))
        self.total_value.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d7;")

        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_value)
        total_layout.addStretch()

        layout.addWidget(total_frame)

        #Статус и кнопки
        status_layout = QHBoxLayout()

        status_label = QLabel("Статус:")
        status_label.setStyleSheet("font-size: 13px; font-weight: bold;")

        self.status_combo = QComboBox()
        for i, v in enumerate(["Оформлен", "В работе", "Готовый к выдаче", "Завершенный", "Отмененный"]):
            self.status_combo.addItem(v, i+1)
        #self.status_combo.addItems(["Оформленный", "В работе", "Готовый к выдаче", "Завершенный", "Отмененный"])
        self.status_combo.setCurrentIndex(self.order_data['status_id']-1)
        self.status_combo.setFixedWidth(150)
        self.status_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 3px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        arrow_label = QLabel("▼")
        arrow_label.setStyleSheet("color: #666; font-size: 10px; margin-left: -20px;")

        status_layout.addWidget(status_label)
        status_layout.addWidget(self.status_combo)
        status_layout.addWidget(arrow_label)
        status_layout.addStretch()

        layout.addLayout(status_layout)

        #Кнопки Ок и Отмена
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("Ок")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)

        layout.addWidget(button_box)

    def populate_items_table(self):
        items = self.order_data.get('product_list', [])
        self.items_table.setRowCount(len(items))

        for row, item in enumerate(items):
            self.items_table.setItem(row, 0, QTableWidgetItem(item['name']))

            quantity_item = QTableWidgetItem(str(item['quantity']))
            quantity_item.setTextAlignment(Qt.AlignCenter)
            self.items_table.setItem(row, 1, quantity_item)

            total_item = QTableWidgetItem(f"{item['total_price']:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.items_table.setItem(row, 2, total_item)

    def get_updated_status(self):
        return {
            "order_id": self.id,
            "status_id": self.status_combo.currentData()
        }


class OrdersScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1200, 600)
        self.orders_data = []

        #Текущий фильтр
        self.current_filter = "Все заказы"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        #Панель статусов
        self.create_status_bar(layout)

        #Панель поиска
        self.create_search_bar(layout)

        #Таблица заказов
        self.create_orders_table(layout)

        #Заполняем таблицу
        self.filter_orders()

        self.table.cellDoubleClicked.connect(self.on_order_double_clicked)

    def load_orders_from_api(self):
            try:
                response = get_emp_orders(employee_id=session_employee_id)

                if isinstance(response, dict) and 'orders' in response:
                    self.orders_data = response['orders']
                else:
                    self.orders_data = response if isinstance(response, list) else []

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить заказы:\n{str(e)}")

    def create_status_bar(self, layout):
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)

        self.status_buttons = {}

        self.status_mapping = {
            "Все заказы": None,
            "Оформлены": 1,
            "В работе": 2,
            "Готовые к выдаче": 3,
            "Завершенные": 4,
            "Отмененные": 5
        }

        for status, i in self.status_mapping.items():
            btn = QPushButton(status)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFlat(True)

            if status == "Все заказы":
                btn.setStyleSheet("""
                    QPushButton {
                        color: #0078d7;
                        border-bottom: 2px solid #0078d7;
                        padding: 5px 0px;
                        font-size: 10px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #666;
                        padding: 5px 0px;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        color: #0078d7;
                    }
                """)

            btn.clicked.connect(lambda checked, s=status: self.on_status_filter_clicked(s))

            self.status_buttons[status] = btn
            status_layout.addWidget(btn)

        status_layout.addStretch()
        layout.addLayout(status_layout)

    def on_status_filter_clicked(self, status):
        self.current_filter = status
        self.filter_orders(status=status, orders_data=self.orders_data)

        for btn_status, btn in self.status_buttons.items():
            if btn_status == status:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #0078d7;
                        border-bottom: 2px solid #0078d7;
                        padding: 5px 0px;
                        font-size: 10px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #666;
                        padding: 5px 0px;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        color: #0078d7;
                    }
                """)

    def filter_orders(self, status = "Все заказы", orders_data = None):
        filter_status = self.status_mapping.get(status)
        if orders_data is None:
            self.load_orders_from_api()
            orders_data = self.orders_data

        if filter_status is None:
            filtered_orders = orders_data
        else:
            filtered_orders = [
                order for order in orders_data
                if order['status_id'] == filter_status
            ]
        self.update_table(filtered_orders)

    def update_table(self, orders_all):
        display_data = []
        for order in orders_all:
            display_data.append([
                order['id'],
                order['user_id'],
                order['total_ammount'],
                order['phone'],
                order['created_at'],
                order['order_datetime'],
                order['status_name'],
            ])

        display_data.sort(key=lambda x: x[0], reverse=True)

        self.table.setRowCount(len(display_data))
        for row, order_data in enumerate(display_data):
            for col, value in enumerate(order_data):
                item = QTableWidgetItem(str(value))

                if col == 6:
                    item.setTextAlignment(Qt.AlignCenter)
                    self.color_status_item(item, value)
                    
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

    def color_status_item(self, item, status):
        colors = {
            "Оформлен": ("#28a745", "#e8f5e9"),
            "В работе": ("#ff8c00", "#fff3e0"),
            "Готовый к выдаче": ("#0078d7", "#e6f2fa"),
            "Завершенный": ("#6c757d", "#f8f9fa"),
            "Отмененный": ("#dc3545", "#f8d7da")
        }

        if status in colors:
            item.setForeground(QColor(colors[status][0]))
            item.setBackground(QColor(colors[status][1]))

    def create_search_bar(self, layout):
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по номеру заказа, имени пользователя или телефону...")
        self.search_input.setFixedHeight(30)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 12px;
            }
        """)

        search_btn = QPushButton("Найти")
        search_btn.setFixedSize(70, 30)
        search_btn.setCursor(Qt.PointingHandCursor)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }
        """)
        search_btn.clicked.connect(self.search_orders)

        #Кнопка сброса поиска
        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(30, 30)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        clear_btn.clicked.connect(self.clear_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(clear_btn)
        search_layout.addStretch()

        layout.addLayout(search_layout)

    def clear_search(self):
        self.search_input.clear()
        self.filter_orders(self.current_filter)

    def create_orders_table(self, layout):
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "№ Заказа", "ID пользователя", "Сумма заказа",
            "Телефон", "Дата создания", "Дата выполнения", "Статус"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                selection-background-color: #e6f2fa;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 6px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                font-size: 11px;       
            }
        """)

        layout.addWidget(self.table)

    def on_order_double_clicked(self, row, column):
        order_data = get_order(self.orders_data, int(self.table.item(row, 0).text())) 
        dialog = OrderDetailDialog(order_data, self)
        if dialog.exec() == QDialog.Accepted:
            try:
                new_status = dialog.get_updated_status()
                put_order_update(new_status)
                self.filter_orders(self.current_filter)
                QMessageBox.information(self, "Успешно", f"Статус заказа '{dialog.id}' обновлён!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Статус заказа '{order_data['id']}' не обновлён:\n{str(e)}")

    def search_orders(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.filter_orders(self.current_filter)
            return

        filter_status = self.status_mapping.get(self.current_filter)
        if filter_status is None:
            current_orders = self.orders_data
        else:
            current_orders = [
                order for order in self.orders_data
                if order['status_id'] == filter_status
            ]

        #Поиск по тексту
        filtered_orders = []
        for order in current_orders:
            if (search_text in str(order['id']).lower() or  #Поиск по номеру
                    search_text in str(order['user_id']).lower() or  #Поиск по имени
                    search_text in str(order['phone']).lower()):  #Поиск по телефону
                filtered_orders.append(order)

        if filtered_orders:
            self.update_table(filtered_orders)
        else:
            QMessageBox.information(self, "Поиск", "Ничего не найдено")
            self.filter_orders(self.current_filter)


class AddProductDialog(QDialog):
    def __init__(self, parent=None, tag=None, product_data=None):
        super().__init__(parent)

        self.tag = tag
        self.data = product_data

        self.catalogPage = parent
        self.products_data = self.catalogPage.products_data
        self.categories_data = self.catalogPage.categories_data

        self.id = None

        self.selected_image_path = None

        if self.tag is None:
            self.tag = 'C'
            

        if self.tag == "C":
            self.setWindowTitle("Добавить изделие")
            self.setMinimumSize(800, 600)
            self.setModal(True)

        elif self.tag == "R":
            self.id = self.data['id']
            self.setWindowTitle(f"Просмотр изделия: {self.data['name']}")
            self.setMinimumSize(800, 600)
            self.setModal(True)


        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #0078d7;
            }
            QCheckBox::indicator:checked {
            border: 1px solid #0078d7;
            background-color: #0078d7;
            border-radius: 3px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        #Заголовок
        title = QLabel(f"Добавление изделия")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title)

        #Форма
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)

        #Устанавливаем пропорции столбцов
        form_layout.setColumnStretch(0, 1)  # Левые метки
        form_layout.setColumnStretch(1, 2)  # Поля ввода в левой части
        form_layout.setColumnStretch(2, 1)  # Правые метки
        form_layout.setColumnStretch(3, 2)  # Поля ввода в правой части

        #Наименование
        form_layout.addWidget(QLabel("Наименование:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите наименование изделия")
        form_layout.addWidget(self.name_input, 0, 1, 1, 3)

        #Категория
        form_layout.addWidget(QLabel("Категория:"), 1, 0)
        self.category_combo = QComboBox()
        
        for c in self.categories_data:
            self.category_combo.addItem(c['category_name'], c['id'])
        self.category_combo.setEditable(True)
        form_layout.addWidget(self.category_combo, 1, 1)

        #Количество на складе
        form_layout.addWidget(QLabel("Вес:"), 1, 2)
        self.weight_spin = QSpinBox()
        self.weight_spin.setRange(0, 10000)
        self.weight_spin.setSuffix(" г")
        form_layout.addWidget(self.weight_spin, 1, 3)

        #Цена
        form_layout.addWidget(QLabel("Цена:"), 2, 0)
        self.selling_price = QDoubleSpinBox()
        self.selling_price.setRange(0, 1000)
        self.selling_price.setPrefix("₽ ")
        self.selling_price.setDecimals(2)
        form_layout.addWidget(self.selling_price, 2, 1)

        #Себестоимость
        form_layout.addWidget(QLabel("Себестоимость:"), 2, 2)
        self.cost_price = QDoubleSpinBox()
        self.cost_price.setRange(0, 1000)
        self.cost_price.setPrefix("₽ ")
        self.cost_price.setDecimals(2)
        form_layout.addWidget(self.cost_price, 2, 3)

        #Описание
        form_layout.addWidget(QLabel("Описание:"), 3, 0)
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Введите описание изделия")
        form_layout.addWidget(self.desc_input, 3, 1, 1, 3)

        #Состав
        form_layout.addWidget(QLabel("Состав:"), 4, 0)
        self.ingredients_input = QLineEdit()
        self.ingredients_input.setPlaceholderText("Введите состав изделия")
        form_layout.addWidget(self.ingredients_input, 4, 1, 1, 3)

        #Энергетическая ценность
        form_layout.addWidget(QLabel("Энергетическая ценность:"), 5, 0)
        self.calories_spin = QSpinBox()
        self.calories_spin.setRange(0, 10000)
        self.calories_spin.setSuffix(" ккал")
        form_layout.addWidget(self.calories_spin, 5, 1)

        #Жиры
        form_layout.addWidget(QLabel("Жиры:"), 5, 2)
        self.fats_spin = QDoubleSpinBox()
        self.fats_spin.setRange(0, 1000)
        self.fats_spin.setSuffix(" г")
        self.fats_spin.setDecimals(1)
        form_layout.addWidget(self.fats_spin, 5, 3)

        #Белки
        form_layout.addWidget(QLabel("Белки:"), 6, 0)
        self.proteins_spin = QDoubleSpinBox()
        self.proteins_spin.setRange(0, 1000)
        self.proteins_spin.setSuffix(" г")
        self.proteins_spin.setDecimals(1)
        form_layout.addWidget(self.proteins_spin, 6, 1)

        #Углеводы
        form_layout.addWidget(QLabel("Углеводы:"), 6, 2)
        self.carbs_spin = QDoubleSpinBox()
        self.carbs_spin.setRange(0, 1000)
        self.carbs_spin.setSuffix(" г")
        self.carbs_spin.setDecimals(1)
        form_layout.addWidget(self.carbs_spin, 6, 3)

        #Изображение
        self.pic_button = QPushButton("Загрузить изображение")
        self.pic_button.setCursor(Qt.PointingHandCursor)
        self.pic_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.pic_button.clicked.connect(self.load_image)
        form_layout.addWidget(self.pic_button, 8, 0, 1, 2)

        #Метка для отображения пути к файлу
        self.image_path_label = QLabel("Файл не выбран")
        self.image_path_label.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        form_layout.addWidget(self.image_path_label, 8, 2, 1, 2)

        layout.addWidget(form_widget)

        #Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("Добавить")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)

        #Отображение
        self.show_on_display = QCheckBox("Отображать изделие")
        self.show_on_display.setChecked(True)
        layout.addWidget(self.show_on_display)

        if self.tag == "R":
            title.setText(f"Просмотр изделия: {self.data['name']} | ID: {self.id}")
            ok_button.setText("Сохранить")
            self.name_input.setText(self.data['name'])
            i = self.category_combo.findData(self.data['category_id'])
            self.category_combo.setCurrentIndex(i)
            self.selling_price.setValue(self.data['sale_price'])
            self.cost_price.setValue(self.data['cost_price'])
            self.ingredients_input.setText(self.data['composition'])
            self.desc_input.setText(self.data['description'])
            self.calories_spin.setValue(self.data['calories'])
            self.proteins_spin.setValue(self.data['protein'])
            self.fats_spin.setValue(self.data['fat'])
            self.carbs_spin.setValue(self.data['carbs'])
            self.weight_spin.setValue(self.data['weight'])
            self.show_on_display.setChecked(self.data['is_visible'])
            self.selected_image_path = None

        layout.addWidget(button_box)

    def load_image(self):
        from PySide6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif);;Все файлы (*.*)"
        )

        if file_path:
            self.selected_image_path = file_path
            file_name = os.path.basename(file_path)
            self.image_path_label.setText(f"✓ {file_name}")
            self.image_path_label.setStyleSheet("color: #28a745; font-size: 11px; padding: 5px;")
            self.pic_button.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 8px 20px;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 150px;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
        else:
            self.selected_image_path = None

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите наименование изделия")
            self.name_input.setFocus()
            return
        if not self.category_combo.currentText().strip():
            QMessageBox.warning(self, "Ошибка", "Выберите категорию изделия")
            self.category_combo.setFocus()
            return
        if self.cost_price.value() <= 0:
            QMessageBox.warning(self, "Ошибка", "Введите корректную себестоимость")
            self.cost_price.setFocus()
            return
        if self.selling_price.value() <= 0:
            QMessageBox.warning(self, "Ошибка", "Введите корректную цену")
            self.selling_price.setFocus()
            return

        self.accept()

    def get_product_data(self):
        data = {
            "name": self.name_input.text().strip(),
            "category_id": self.category_combo.currentData(),
            "sale_price": self.selling_price.value(),
            "cost_price": self.cost_price.value(),
            "composition": self.ingredients_input.text().strip(),
            "description": self.desc_input.text().strip(),
            "calories": self.calories_spin.value(),
            "protein": self.proteins_spin.value(),
            "fat": self.fats_spin.value(),
            "carbs": self.carbs_spin.value(),
            "weight": self.weight_spin.value(),
            "is_visible": self.show_on_display.isChecked(),
            'product_id': self.id,
            "image_url": self.selected_image_path,
        }
        return data


class AddCategoryDialog(QDialog):
    def __init__(self, parent=None, tag=None, category_data=None):
        super().__init__(parent)

        self.tag = tag
        self.data = category_data

        if self.tag is None:
            self.tag = 'C'
            
        self.catalogPage = parent
        self.categories_data = self.catalogPage.categories_data

        self.id = None

        if self.tag == "C":
            self.setWindowTitle("Добавить категорию")
            self.setMinimumSize(400, 300)
            self.setModal(True)

        elif self.tag == "R":
            self.id = self.data['id']
            self.setWindowTitle(f"Просмотр категории: {self.id}")
            self.setMinimumSize(500, 350)
            self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border-color: #0078d7;
            }
            QCheckBox::indicator:checked {
            border: 1px solid #0078d7;
            background-color: #0078d7;
            border-radius: 3px;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        #Заголовок
        title = QLabel("Добавление категории")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title)

        #Форма
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)

        #Наименование категории
        form_layout.addWidget(QLabel("Наименование категории:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите наименование категории")
        form_layout.addWidget(self.name_input, 0, 1)

        #Порядок категории
        form_layout.addWidget(QLabel("Порядок категории:"), 1, 0)
        self.order_spin = QSpinBox()
        self.order_spin.setValue(max([i['showing_number'] for i in self.categories_data]) + 1)
        self.order_spin.setRange(1, 100)
        self.order_spin.setSuffix("")
        form_layout.addWidget(self.order_spin, 1, 1)

        layout.addWidget(form_widget)

        #Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("Добавить")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)

        #Отображение
        self.show_on_display = QCheckBox("Отображать категорию")
        self.show_on_display.setChecked(False)
        layout.addWidget(self.show_on_display) 

        if self.tag == "R":
            self.name_input.setText(self.data['category_name'])
            self.order_spin.setValue(self.data['showing_number'])
            title.setText(f"Категория: {self.data['category_name']}")
            ok_button.setText("Cохранить")
            self.show_on_display.setChecked(self.data['display_on_site'])

        layout.addWidget(button_box)

    def validate_and_accept(self):
        new_name = self.name_input.text().strip()
        new_order = self.order_spin.value()

        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите наименование категории")
            self.name_input.setFocus()
            return
        
        for cat in self.categories_data:
            if self.tag == "C":
                if cat['category_name'] == self.name_input.text().strip():
                    QMessageBox.warning(self, "Ошибка", "Категория с таким названием существует")
                    self.name_input.setFocus()
                    return
                if cat['showing_number'] == self.order_spin.value():
                    QMessageBox.warning(self, "Ошибка", "Категория такого порядка существует")
                    self.order_spin.setFocus()
                    return
                
            elif self.tag == "R":
                if cat['category_name'] != new_name and cat['category_name'] == self.name_input.text().strip():
                    QMessageBox.warning(self, "Ошибка", "Категория с таким названием существует")
                    self.name_input.setFocus()
                    return
                if cat['showing_number'] != new_order and cat['showing_number'] == self.order_spin.value():
                    QMessageBox.warning(self, "Ошибка", "Категория такого порядка существует")
                    self.order_spin.setFocus()
                    return

        self.accept()

    def get_category_data(self):
        return {
          'category_name': self.name_input.text().strip(), 
          'showing_number': self.order_spin.value(), 
          'display_on_site': self.show_on_display.isChecked(),
          'id': self.id
        }


class CatalogPage(QWidget):
    def __init__(self):
        super().__init__()
        #Данные для изделий
        self.products_data = [] 
        self.load_products_from_api()

        #Данные для категорий
        self.categories_data = []
        self.load_categories_from_api()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        #Панель статусов
        self.create_status_bar(layout)

        #Стек для разделов каталога
        self.catalog_stack = QStackedWidget()

        #Страница изделий
        self.products_page = self.create_products_page()

        #Страница категорий
        self.categories_page = self.create_categories_page()

        self.catalog_stack.addWidget(self.products_page)
        self.catalog_stack.addWidget(self.categories_page)

        layout.addWidget(self.catalog_stack)

    def load_products_from_api(self):
        try:
            response = get_products()

            if isinstance(response, dict) and 'products' in response:
                self.products_data = response['products']
            else:
                self.products_data = response if isinstance(response, list) else []

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить изделия:\n{str(e)}")

    def load_categories_from_api(self):
        try:
            response = get_categories()
            if isinstance(response, dict) and 'categories' in response:
                self.categories_data = response['categories']
            else:
                self.categories_data = response if isinstance(response, list) else []
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить категории:\n{str(e)}")

    def create_status_bar(self, layout):
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)

        self.status_buttons = {}
        statuses = ["Изделия", "Категории изделий"]

        for status in statuses:
            btn = QPushButton(status)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFlat(True)

            if status == "Изделия":
                btn.setStyleSheet("""
                    QPushButton {
                        color: #0078d7;
                        border-bottom: 2px solid #0078d7;
                        padding: 5px 0px;
                        font-size: 10px;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #666;
                        padding: 5px 0px;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        color: #0078d7;
                    }
                """)

            btn.clicked.connect(lambda checked, s=status: self.on_status_filter_clicked(s))
            self.status_buttons[status] = btn
            status_layout.addWidget(btn)

        status_layout.addStretch()
        layout.addLayout(status_layout)

    def on_status_filter_clicked(self, status):
        if status == "Изделия":
            self.catalog_stack.setCurrentWidget(self.products_page)
        elif status == "Категории изделий":
            self.catalog_stack.setCurrentWidget(self.categories_page)

        for btn_status, btn in self.status_buttons.items():
            if btn_status == status:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #0078d7;
                        border-bottom: 2px solid #0078d7;
                        padding: 5px 0px;
                        font-size: 10px;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #666;
                        padding: 5px 0px;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        color: #0078d7;
                    }
                """)

    #СТРАНИЦА ИЗДЕЛИЙ
    def create_products_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        title = QLabel("Все изделия")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title)

        # Поиск и кнопки для изделий
        search_layout = QHBoxLayout()

        self.products_search = QLineEdit()
        self.products_search.setPlaceholderText("Поиск по артикулу, названию или категории...")
        self.products_search.setFixedHeight(35)
        self.products_search.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)

        search_btn = QPushButton("Поиск")
        search_btn.setFixedSize(80, 35)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        search_btn.clicked.connect(self.search_products)

        add_btn = QPushButton("+ Добавить изделие")
        add_btn.setFixedHeight(35)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_btn.clicked.connect(self.show_add_product_dialog)

        #Кнопка сброса поиска
        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(30, 30)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        clear_btn.clicked.connect(self.clear_products_search)

        search_layout.addWidget(self.products_search)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(clear_btn)
        search_layout.addStretch()
        search_layout.addWidget(add_btn)

        layout.addLayout(search_layout)

        #Таблица изделий
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels([
            "Артикул", "Наименование", "Категория", "Себестоимость", "Цена"
        ])

        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.cellDoubleClicked.connect(self.on_product_double_clicked)

        self.products_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                selection-background-color: #e6f2fa;
                font-size: 12px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                font-size: 11px;
                color: #333;
            }
        """)

        self.populate_products_table(self.products_data)
        layout.addWidget(self.products_table)
        return page

    def on_product_double_clicked(self, row, col):
        product_data = get_product(self.products_data, int(self.products_table.item(row, 0).text()))
        dialog = AddProductDialog(self, tag='R', product_data=product_data)
        if dialog.exec() == QDialog.Accepted:
            try:
                product_data = dialog.get_product_data()
                put_product(product_data)
                self.populate_products_table()
                QMessageBox.information(self, "Успешно", f"Изделие '{product_data['name']}' обновлено!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Изделие '{product_data['name']}' не обновлено:\n{str(e)}")


    def populate_products_table(self, data=None):
        if data is None:
            self.load_products_from_api()
            data = self.products_data

        self.products_table.setRowCount(len(data))

        for row, item_data in enumerate(data):
            # Артикул 
            id_item = QTableWidgetItem(str(item_data.get('id', '')))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.products_table.setItem(row, 0, id_item)

            # Наименование
            self.products_table.setItem(row, 1, QTableWidgetItem(item_data.get('name', '')))

            # Категория
            self.products_table.setItem(row, 2, QTableWidgetItem(*[c['category_name'] for c in self.categories_data if c['id'] == item_data.get('category_id', '')])) 
            
            # Себестоимость
            cost_item = QTableWidgetItem(str(item_data.get('cost_price', '')))
            cost_item.setTextAlignment(Qt.AlignCenter)
            self.products_table.setItem(row, 3, cost_item)

            # Цена
            sale_item = QTableWidgetItem(str(item_data.get('sale_price', '')))
            sale_item.setTextAlignment(Qt.AlignCenter)
            self.products_table.setItem(row, 4, sale_item)

    def search_products(self):
        search_text = self.products_search.text().lower()
        if not search_text:
            self.populate_products_table()
            return

        filtered_data = []
        for item in self.products_data:
            if (search_text in str(item['id']) or  #Поиск по артикулу
                search_text in item['name'].lower() or  #Поиск по названию
                search_text in [c['category_name'] for c in self.categories_data if c['id'] == item['category_id']][0].lower()):  #Поиск по категории
                filtered_data.append(item)

        if filtered_data:
            self.populate_products_table(filtered_data)
        else:
            QMessageBox.information(self, "Поиск", "Ничего не найдено")
            self.populate_products_table()

    def clear_products_search(self):
        self.products_search.clear()
        self.populate_products_table()

    def show_add_product_dialog(self):
        dialog = AddProductDialog(self)
        if dialog.exec() == QDialog.Accepted:
            try:
                product_data = dialog.get_product_data()
                post_product(product_data)
                self.populate_products_table()
                QMessageBox.information(self, "Успешно", f"Изделие '{product_data['name']}' добавлено!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Изделие '{product_data['name']}' не добавлено:\n{str(e)}")

    #СТРАНИЦА КАТЕГОРИЙ
    def create_categories_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        title = QLabel("Все категории")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title)

        #Поиск и кнопки для категорий
        search_layout = QHBoxLayout()

        self.categories_search = QLineEdit()
        self.categories_search.setPlaceholderText("Поиск по наименованию категории...")
        self.categories_search.setFixedHeight(35)
        self.categories_search.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)

        search_btn = QPushButton("Поиск")
        search_btn.setFixedSize(80, 35)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        search_btn.clicked.connect(self.search_categories)

        add_btn = QPushButton("+ Добавить категорию")
        add_btn.setFixedHeight(35)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_btn.clicked.connect(self.show_add_category_dialog)

        #Кнопка сброса поиска
        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(30, 30)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        clear_btn.clicked.connect(self.clear_categories_search)

        search_layout.addWidget(self.categories_search)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(clear_btn)
        search_layout.addStretch()
        search_layout.addWidget(add_btn)

        layout.addLayout(search_layout)

        #Таблица категорий
        self.categories_table = QTableWidget()
        self.categories_table.setColumnCount(3)
        self.categories_table.setHorizontalHeaderLabels([
            "Наименование категории изделий", "Порядок категории", "ID"
        ])

        self.categories_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.categories_table.horizontalHeader().setStretchLastSection(True)
        self.categories_table.verticalHeader().setVisible(False)
        self.categories_table.setAlternatingRowColors(True)
        self.categories_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.categories_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.categories_table.cellDoubleClicked.connect(self.on_category_double_clicked)

        self.categories_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                selection-background-color: #e6f2fa;
                font-size: 12px;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                font-size: 11px;
                color: #333;
            }
        """)

        self.populate_categories_table(self.categories_data)
        layout.addWidget(self.categories_table)
        return page

    def on_category_double_clicked(self, row, column):
        category_data = get_category(self.categories_data, int(self.categories_table.item(row, 2).text()))
        dialog = AddCategoryDialog(self, tag='R', category_data=category_data)
        if dialog.exec() == QDialog.Accepted:
            try:
                category_data = dialog.get_category_data()
                put_category(category_data)
                self.populate_categories_table()
                QMessageBox.information(self, "Успешно", f"Категория '{category_data['category_name']}' обновлена!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Категория '{category_data['category_name']}' не обновлена:\n{str(e)}")

    def populate_categories_table(self, data=None):
        if data is None:
            self.load_categories_from_api()
            data = self.categories_data

        self.categories_table.setRowCount(len(data))

        for row, cat_data in enumerate(data):
            # Наименование
            name_item = QTableWidgetItem(str(cat_data.get('category_name', '')))
            name_item.setTextAlignment(Qt.AlignCenter)
            self.categories_table.setItem(row, 0, name_item)

            # Порядок
            showing_item = QTableWidgetItem(str(cat_data.get('showing_number', '')))
            showing_item.setTextAlignment(Qt.AlignCenter)
            self.categories_table.setItem(row, 1, showing_item)

            # ID
            id_item = QTableWidgetItem(str(cat_data.get('id', '')))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.categories_table.setItem(row, 2, id_item)

    def search_categories(self):
        search_text = self.categories_search.text().lower()
        if not search_text:
            self.populate_categories_table()
            return

        filtered_data = []
        for cat in self.categories_data:
            if search_text in cat['category_name'].lower():
                filtered_data.append(cat)

        if filtered_data:
            self.populate_categories_table(filtered_data)
        else:
            QMessageBox.information(self, "Поиск", "Ничего не найдено")
            self.populate_categories_table()

    def clear_categories_search(self):
        self.categories_search.clear()
        self.populate_categories_table()

    def show_add_category_dialog(self):
        dialog = AddCategoryDialog(self, tag="C")
        if dialog.exec() == QDialog.Accepted:
            try:
                category_data = dialog.get_category_data()
                post_category(category_data)
                self.populate_categories_table()
                QMessageBox.information(self, "Успешно", f"Категория '{category_data['category_name']}' добавлена!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Категория '{category_data['category_name']}' не добавлена:\n{str(e)}")
        

class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.branches_data = get_branches()['branches']
        self.employees_data = get_employees()['employees']

        self.setWindowTitle("Добавить сотрудника")
        self.setMinimumSize(500, 500)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #0078d7;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        #Заголовок
        title = QLabel(f"Добавление сотрудника")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title)

        #Форма
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)

        #Фамилия
        form_layout.addWidget(QLabel("Фамилия:"), 0, 0)
        self.lastname_input = QLineEdit()
        self.lastname_input.setPlaceholderText("Введите фамилию сотрудника")
        form_layout.addWidget(self.lastname_input, 0, 1)

        #Имя
        form_layout.addWidget(QLabel("Имя:"), 1, 0)
        self.firstname_input = QLineEdit()
        self.firstname_input.setPlaceholderText("Введите имя сотрудника")
        form_layout.addWidget(self.firstname_input, 1, 1)

        #Отчество
        form_layout.addWidget(QLabel("Отчество:"), 2, 0)
        self.patronymic_input = QLineEdit()
        self.patronymic_input.setPlaceholderText("Введите отчество сотрудника")
        form_layout.addWidget(self.patronymic_input, 2, 1)

        #Логин
        form_layout.addWidget(QLabel("Логин:"), 3, 0)
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите логин сотрудника")
        form_layout.addWidget(self.login_input, 3, 1)

        #Пароль
        form_layout.addWidget(QLabel("Пароль:"), 4, 0)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль сотрудника")
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_input, 4, 1)

        #Телефон
        form_layout.addWidget(QLabel("Телефон:"), 5, 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+7(999)123-45-67")
        self.phone_input.setInputMask("+7(999)999-99-99")
        form_layout.addWidget(self.phone_input, 5, 1)

        #Должность
        form_layout.addWidget(QLabel("Должность:"), 7, 0)
        self.position_combo = QComboBox()
        for i, p in enumerate(["Администратор", "Менеджер"]):
            self.position_combo.addItem(p, i+1)
        form_layout.addWidget(self.position_combo, 7, 1)

        #Адрес филиала
        form_layout.addWidget(QLabel("Адресс филиала:"), 9, 0)
        self.work_address = QLabel()
        form_layout.addWidget(self.work_address, 9, 1)

        #Филиал
        form_layout.addWidget(QLabel("Филиал:"), 8, 0)
        self.branch_combo = QComboBox()
        for br in self.branches_data:
            self.branch_combo.addItem(br['branches_name'], br['id'])
        self.on_item_changed()
        self.branch_combo.currentIndexChanged.connect(self.on_item_changed)
        form_layout.addWidget(self.branch_combo, 8, 1)

        layout.addWidget(form_widget)

        #Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("Добавить")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)

        layout.addWidget(button_box)

    def on_item_changed(self):
        name = self.branch_combo.currentData()
        for branch in self.branches_data:
            if branch['id'] == name:
                name = branch['branches_address']
                break
        self.work_address.setText(name)

    def validate_and_accept(self):
        if not self.lastname_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите фамилию сотрудника")
            self.lastname_input.setFocus()
            return

        if not self.firstname_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите имя сотрудника")
            self.firstname_input.setFocus()
            return

        if not self.phone_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите телефон сотрудника")
            self.phone_input.setFocus()
            return
        
        if not bool(re.match(r"^\+\d{1,3}\(\d{3}\)\d{3}\-\d{2}\-\d{2}$" ,self.phone_input.text().strip())):
            QMessageBox.warning(self, "Ошибка", "Введите телефон сотрудника корректно")
            self.phone_input.setFocus()
            return

        self.accept()

    def get_employee_data(self):
        return {
            'full_name': f'{self.lastname_input.text().strip()} {self.firstname_input.text().strip()} {self.patronymic_input.text().strip()}',
            'phone': self.phone_input.text().strip(),
            'position_id': self.position_combo.currentData(),
            'username': self.login_input.text().strip(),
            'password': self.password_input.text().strip(),
            'branch_id': self.branch_combo.currentData()
        }


class EmployeeDetailDialog(QDialog):
    employee_deleted = Signal(int)

    def __init__(self, employee_data, parent=None):
        super().__init__(parent)

        self.branches_data = get_branches()['branches']

        self.employee_data = employee_data
        self.employee_id = employee_data['id']

        self.fullname = [None, None, None]
        names = self.employee_data['full_name'].split()
        self.fullname[:len(names)] = names

        self.setWindowTitle(f"Сотрудник: {self.employee_id}")
        self.setMinimumSize(500, 550)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLabel[heading="true"] {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-top: 10px;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #0078d7;
            }
            QPushButton#deleteButton {
                background-color: #dc3545;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton#deleteButton:hover {
                background-color: #c82333;
            }
            QPushButton#saveButton {
                background-color: #0078d7;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton#saveButton:hover {
                background-color: #005a9e;
            }
            QPushButton#cancelButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton#cancelButton:hover {
                background-color: #5a6268;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        #Заголовок с ФИО сотрудника
        title_label = QLabel(f"Сотрудник: {self.employee_data['full_name']}")
        title_label.setProperty("heading", True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title_label)

        #Информация о сотруднике
        info_group = QGroupBox("Информация о сотруднике")
        info_layout = QGridLayout(info_group)
        info_layout.setVerticalSpacing(10)
        info_layout.setHorizontalSpacing(20)

        #ID сотрудника
        info_layout.addWidget(QLabel("ID:"), 0, 0)
        id_label = QLabel(f"<b>{self.employee_data['id']}</b>")
        info_layout.addWidget(id_label, 0, 1)

        #Фамилия
        info_layout.addWidget(QLabel("Фамилия:"), 1, 0)
        self.lastname_input = QLineEdit(self.fullname[0])
        info_layout.addWidget(self.lastname_input, 1, 1)

        #Имя
        info_layout.addWidget(QLabel("Имя:"), 2, 0)
        self.firstname_input = QLineEdit(self.fullname[1])
        info_layout.addWidget(self.firstname_input, 2, 1)

        #Отчество
        info_layout.addWidget(QLabel("Отчество:"), 3, 0)
        self.patronymic_input = QLineEdit(self.fullname[2])
        info_layout.addWidget(self.patronymic_input, 3, 1)

        #Логин
        info_layout.addWidget(QLabel("Логин:"), 4, 0)
        self.login_input = QLineEdit(self.employee_data['username'])
        info_layout.addWidget(self.login_input, 4, 1)

        #Телефон
        info_layout.addWidget(QLabel("Телефон:"), 5, 0)
        self.phone_input = QLineEdit(self.employee_data['phone'])
        self.phone_input.setInputMask("+7(000)000-00-00")
        info_layout.addWidget(self.phone_input, 5, 1)

        #Должность
        info_layout.addWidget(QLabel("Должность:"), 7, 0)
        self.position_combo = QComboBox()
        for i, p in enumerate(["Администратор", "Менеджер"]):
            self.position_combo.addItem(p, i+1)
        i = self.position_combo.findData(self.employee_data['position_id'])
        self.position_combo.setCurrentIndex(i)
        info_layout.addWidget(self.position_combo, 7, 1)

        #Адрес филиала
        info_layout.addWidget(QLabel("Адресс филиала:"), 9, 0)
        self.work_address = QLabel()
        info_layout.addWidget(self.work_address, 9, 1)

        #Филиал
        info_layout.addWidget(QLabel("Филиал:"), 8, 0)
        self.branch_combo = QComboBox()
        for br in self.branches_data:
            self.branch_combo.addItem(br['branches_name'], br['id'])
        i = self.branch_combo.findData(self.employee_data['branch_id'])
        self.branch_combo.setCurrentIndex(i)
        self.on_item_changed()
        self.branch_combo.currentIndexChanged.connect(self.on_item_changed)
        info_layout.addWidget(self.branch_combo, 8, 1)

        layout.addWidget(info_group)

        #Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setObjectName("saveButton")
        self.save_button.clicked.connect(self.save_employee)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_employee)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def on_item_changed(self):
        name = self.branch_combo.currentData()
        for branch in self.branches_data:
            if branch['id'] == name:
                name = branch['branches_address']
                break
        self.work_address.setText(name)

    def save_employee(self):
        #Проверка обязательных полей
        if not self.lastname_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите фамилию сотрудника")
            self.lastname_input.setFocus()
            return

        if not self.firstname_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите имя сотрудника")
            self.firstname_input.setFocus()
            return

        if not self.phone_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите телефон сотрудника")
            self.phone_input.setFocus()
            return
        
        if not bool(re.match(r"^\+\d{1,3}\(\d{3}\)\d{3}\-\d{2}\-\d{2}$" ,self.phone_input.text().strip())):
            QMessageBox.warning(self, "Ошибка", "Введите телефон сотрудника корректно")
            self.phone_input.setFocus()
            return

        self.accept()

    def delete_employee(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить сотрудника {self.fullname[0]} {self.fullname[1]}?\n\nЭто действие нельзя отменить.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.employee_deleted.emit(int(self.employee_id))
            self.reject()

    def get_updated_data(self):
        return {
            'id': self.employee_id,
            'full_name': f'{self.lastname_input.text().strip()} {self.firstname_input.text().strip()} {self.patronymic_input.text().strip()}',
            'phone': self.phone_input.text().strip(),
            'position_id': self.position_combo.currentData(),
            'username': self.login_input.text().strip(),
            'branch_id': self.branch_combo.currentData(),
            'work_address': self.work_address.text()
        }


class EmployeesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.employees_data = get_employees()

        #self.next_id = len(self.all_employees_data) + 1

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        #Заголовок
        title = QLabel("Все сотрудники")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title)

        #Поиск
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по ФИО, должности или телефону...")
        self.search_input.setFixedHeight(35)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)

        search_btn = QPushButton("Поиск")
        search_btn.setFixedSize(80, 35)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        search_btn.clicked.connect(self.search_employees)

        add_btn = QPushButton("+ Добавить сотрудника")
        add_btn.setFixedHeight(35)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_btn.clicked.connect(self.show_add_employee_dialog)

        #Кнопка сброса поиска
        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(30, 30)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        clear_btn.clicked.connect(self.clear_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(clear_btn)
        search_layout.addStretch()
        search_layout.addWidget(add_btn)

        layout.addLayout(search_layout)

        #Таблица сотрудников
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Фамилия", "Имя", "Отчество", "Телефон", "Должность"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.on_employee_double_clicked)

        self.populate_employees()

        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                selection-background-color: #e6f2fa;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 6px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                font-size: 11px;       
            }
        """)

        layout.addWidget(self.table)

    def load_employees_from_api(self):
        try:
            response = get_employees()

            if isinstance(response, dict) and 'employees' in response:
                self.employees_data = response['employees']
            else:
                self.employees_data = response if isinstance(response, list) else []

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить сотрудников:\n{str(e)}")

    def populate_employees(self, data=None):
        if data is None:
            self.load_employees_from_api()
            data = self.employees_data

        self.table.setRowCount(len(data))


        for row, emp_data in enumerate(data):
            fullname = [None, None, None]
            names = emp_data['full_name'].split()
            fullname[:len(names)] = names

            # ID
            id_item = QTableWidgetItem(str(emp_data.get('id', '')))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, id_item)

            # Фамилия
            self.table.setItem(row, 1, QTableWidgetItem(str(fullname[0])))
            
            # Имя
            self.table.setItem(row, 2, QTableWidgetItem(str(fullname[1])))

            # Отчество
            self.table.setItem(row, 3, QTableWidgetItem(str(fullname[2])))

            # Телефон
            self.table.setItem(row, 4, QTableWidgetItem(str(emp_data.get('phone', ''))))

            # Должность
            self.table.setItem(row, 5, QTableWidgetItem(str(emp_data.get('position_name', ''))))
            

    def search_employees(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.populate_employees()
            return

        filtered_data = []
        for emp in self.employees_data:
            full_name = emp['full_name'].lower()
            if (
                    search_text in full_name or  # Поиск по ФИО
                    search_text in emp['phone'].lower() or  # Поиск по телефону
                    search_text in emp['position_name'].lower()):  # Поиск по должности
                filtered_data.append(emp)

        if filtered_data:
            self.populate_employees(filtered_data)
        else:
            QMessageBox.information(self, "Поиск", "Ничего не найдено")

    def clear_search(self):
        self.search_input.clear()
        self.populate_employees()

    def show_add_employee_dialog(self):
        dialog = AddEmployeeDialog(self)
        if dialog.exec() == QDialog.Accepted:
            try: 
                employee_data = dialog.get_employee_data()
                self.add_employee(employee_data)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Сотрудник '{employee_data['full_name']}' не добавлен:\n{str(e)}")

    def add_employee(self, data):
        post_employee(data=data)
        QMessageBox.information(self, "Успешно", f"Сотрудник {data['full_name']} добавлен!")
        self.populate_employees()

    def on_employee_double_clicked(self, row, column):
        employee_id = int(self.table.item(row, 0).text())
        employee_data = get_employee(employee_id=employee_id)['employee']
        dialog = EmployeeDetailDialog(employee_data, self)

        dialog.employee_deleted.connect(self.delete_employee)

        if dialog.exec() == QDialog.Accepted:
            try:
                updated_data = dialog.get_updated_data()
                self.update_employee_data(employee_id, updated_data)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Сотрудник '{employee_data['full_name']}' не обновлён:\n{str(e)}")

    def delete_employee(self, employee_id):
        del_employee(employee_id=employee_id)
        QMessageBox.information(self, "Успешно", f"Сотрудник удален из системы")
        self.populate_employees()

    def update_employee_data(self, employee_id, updated_data):
        put_employee(employee_id=employee_id, data=updated_data)
        QMessageBox.information(self, "Успешно", "Данные сотрудника обновлены")
        self.populate_employees()


class AddBakeryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить филиал")
        self.setMinimumSize(500, 400)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QComboBox, QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus {
                border-color: #0078d7;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(5)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border-color: #0078d7;
            }
            QCheckBox::indicator:checked {
            border: 1px solid #0078d7;
            background-color: #0078d7;
            border-radius: 3px;
            }
        """)

        #Заголовок
        title = QLabel("Добавление филиала")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d7;")
        layout.addWidget(title)

        #Форма
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)

        #Название
        form_layout.addWidget(QLabel("Наименование филиала:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите наименование филиала")
        form_layout.addWidget(self.name_input, 0, 1)

        #Адрес
        form_layout.addWidget(QLabel("Адрес филиала:"), 1, 0)
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Введите полный адрес")
        form_layout.addWidget(self.address_input, 1, 1)

        #Телефон
        form_layout.addWidget(QLabel("Телефон:"), 2, 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+7(999)123-45-67")
        self.phone_input.setInputMask("+7(999)999-99-99")
        form_layout.addWidget(self.phone_input, 2, 1)

        #Статус
        form_layout.addWidget(QLabel("Открыт:"), 4, 0)
        self.status_combo = QCheckBox()
        self.status_combo.setChecked(True)
        form_layout.addWidget(self.status_combo, 4, 1)

        layout.addWidget(form_widget)

        #Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("Добавить")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)

        layout.addWidget(button_box)

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите наименование филиала")
            self.name_input.setFocus()
            return

        if not self.address_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите адрес филиала")
            self.address_input.setFocus()
            return

        if not self.phone_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите телефон филиала")
            self.phone_input.setFocus()
            return

        if not bool(re.match(r"^\+\d{1,3}\(\d{3}\)\d{3}\-\d{2}\-\d{2}$" ,self.phone_input.text().strip())):
            QMessageBox.warning(self, "Ошибка", "Введите телефон филиала корректно")
            self.phone_input.setFocus()
            return
        
        self.accept()

    def get_bakery_data(self):
        return {
            'branches_name': self.name_input.text().strip(),
            'branches_address': self.address_input.text().strip(),
            'branches_phone': self.phone_input.text().strip(),
            'is_active_for_order': self.status_combo.isChecked()
        }


class BakeryDetailDialog(QDialog):
    def __init__(self, branch_data, parent=None):
        super().__init__(parent)
        self.branch_id = branch_data.get('id', 0)
        self.branch_name = branch_data.get('branches_name', '')
        self.branch_address = branch_data.get('branches_address', '')
        self.branch_phone = branch_data.get('branches_phone', '')
        self.branch_status = branch_data.get('is_active_for_order', True)

        self.setWindowTitle(f"Филиал: {self.branch_name}")
        self.setMinimumSize(500, 450)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #0078d7;
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(5)

        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QSpinBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QSpinBox:focus {
                border-color: #0078d7;
            }
            QCheckBox::indicator:checked {
            border: 1px solid #0078d7;
            background-color: #0078d7;
            border-radius: 3px;
            }
        """)

        # Заголовок
        title_label = QLabel(f"Филиал: {self.branch_name} | ID: {self.branch_id}")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d7;")
        layout.addWidget(title_label)

        # Форма
        form_widget = QWidget()
        form_layout = QGridLayout(form_widget)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)

        # Название (только чтение)
        form_layout.addWidget(QLabel("Наименование:"), 0, 0)
        name_label = QLabel(self.branch_name)
        name_label.setStyleSheet("font-weight: bold; color: #0078d7;")
        form_layout.addWidget(name_label, 0, 1)

        # Адрес
        form_layout.addWidget(QLabel("Адрес:*"), 1, 0)
        self.address_input = QLineEdit(self.branch_address)
        self.address_input.setPlaceholderText("Введите полный адрес")
        form_layout.addWidget(self.address_input, 1, 1)

        # Телефон
        form_layout.addWidget(QLabel("Телефон:*"), 2, 0)
        self.phone_input = QLineEdit(self.branch_phone)
        self.phone_input.setPlaceholderText("+7(999)123-45-67")
        self.phone_input.setInputMask("+7(999)999-99-99")
        form_layout.addWidget(self.phone_input, 2, 1)

        # Статус
        form_layout.addWidget(QLabel("Открыт:"), 3, 0)
        self.status_combo = QCheckBox()
        self.status_combo.setChecked(self.branch_status)
        form_layout.addWidget(self.status_combo, 3, 1)

        layout.addWidget(form_widget)

        # Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("Сохранить")
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)

        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setText("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 3px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)

        layout.addWidget(button_box)

    def validate_and_accept(self):
        if not self.address_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите адрес филиала")
            self.address_input.setFocus()
            return

        if not self.phone_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите телефон филиала")
            self.phone_input.setFocus()
            return

        if not bool(re.match(r"^\+\d{1,3}\(\d{3}\)\d{3}\-\d{2}\-\d{2}$" ,self.phone_input.text().strip())):
            QMessageBox.warning(self, "Ошибка", "Введите телефон филиала корректно")
            self.phone_input.setFocus()
            return

        self.accept()

    def get_updated_data(self):
        return {
            'branches_name': self.branch_name,
            'branches_address': self.address_input.text().strip(),
            'branches_phone': self.phone_input.text().strip(),
            'is_active_for_order': self.status_combo.isChecked(),
            'id': self.branch_id
        }


class BakeriesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.bakeries_data = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title = QLabel("Все филиалы")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title)

        # Поиск и кнопки
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию, адресу или телефону филиала...")
        self.search_input.setFixedHeight(35)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
            }
        """)

        search_btn = QPushButton("Поиск")
        search_btn.setFixedSize(80, 35)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        search_btn.clicked.connect(self.search_bakeries)

        add_btn = QPushButton("+ Добавить филиал")
        add_btn.setFixedHeight(35)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        add_btn.clicked.connect(self.show_add_bakery_dialog)


        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(30, 30)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        clear_btn.clicked.connect(self.clear_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addWidget(clear_btn)
        search_layout.addStretch()
        search_layout.addWidget(add_btn)

        layout.addLayout(search_layout)

        # Таблица филиалов
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "ID", "Наименование", "Адрес", "Телефон", "Статус"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.on_bakery_double_clicked)

        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                selection-background-color: #e6f2fa;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 6px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: bold;
                font-size: 11px;       
            }
        """)

        layout.addWidget(self.table)

        # Загружаем данные
        self.populate_bakeries()

    def load_branches_from_api(self):
        try:
            response = get_branches()

            if isinstance(response, dict) and 'branches' in response:
                self.bakeries_data = response['branches']
            else:
                self.bakeries_data = response if isinstance(response, list) else []

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить филиалы:\n{str(e)}")

    def populate_bakeries(self, data=None):
        if data is None:
            self.load_branches_from_api()
            data = self.bakeries_data

        self.table.setRowCount(len(data))

        for row, bakery_data in enumerate(data):
            # ID
            id_item = QTableWidgetItem(str(bakery_data.get('id', '')))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, id_item)

            # Наименование
            self.table.setItem(row, 1, QTableWidgetItem(bakery_data.get('branches_name', '')))

            # Адрес
            self.table.setItem(row, 2, QTableWidgetItem(bakery_data.get('branches_address', '')))

            # Телефон
            self.table.setItem(row, 3, QTableWidgetItem(bakery_data.get('branches_phone', '')))

            # Статус
            status = bakery_data.get('is_active_for_order', True)
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)

            if status == True:
                status_item.setText('Открыт')
                status_item.setForeground(QColor("#28a745"))
                status_item.setBackground(QColor("#e8f5e9"))
            else:
                status_item.setText('Закрыт')
                status_item.setForeground(QColor("#dc3545"))
                status_item.setBackground(QColor("#f8d7da"))

            self.table.setItem(row, 4, status_item)

    def show_add_bakery_dialog(self):
        dialog = AddBakeryDialog(self)
        if dialog.exec() == QDialog.Accepted:
            bakery_data = dialog.get_bakery_data()
            self.add_branch(bakery_data)

    def add_branch(self, data):
        try:
            post_branch(data)
            self.populate_bakeries()
            QMessageBox.information(self, "Успешно", f"Филиал '{data['branches_name']}' добавлен!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить филиал:\n{str(e)}")

    def on_bakery_double_clicked(self, row, column):
        branch_data = self.bakeries_data[row]

        dialog = BakeryDetailDialog(branch_data, self)

        if dialog.exec() == QDialog.Accepted:
            updated_data = dialog.get_updated_data()
            self.update_branch(updated_data)

    def update_branch(self, updated_data):
        try:
            put_branch(updated_data)
            self.populate_bakeries()
            QMessageBox.information(self, "Успешно", "Данные филиала обновлены!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось обновить филиал:\n{str(e)}")

    def search_bakeries(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.populate_bakeries()
            return

        filtered_data = []
        for bakery in self.bakeries_data:
            if (
                    search_text in bakery.get('branches_name', '').lower() or
                    search_text in bakery.get('branches_address', '').lower() or
                    search_text in bakery.get('branches_phone', '').lower()):
                filtered_data.append(bakery)

        if filtered_data:
            self.populate_bakeries(filtered_data)
        else:
            QMessageBox.information(self, "Поиск", "Ничего не найдено")
            self.populate_bakeries()

    def clear_search(self):
        self.search_input.clear()
        self.populate_bakeries()


class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель администратора")
        self.setMinimumSize(1200, 600)

        #Центральный виджет со стеком страниц
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #Верхняя панель
        self.create_top_navbar(main_layout)

        #Стек страниц
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        #Все страницы
        self.orders_page = OrdersScreen()
        self.catalog_page = CatalogPage()
        self.employees_page = EmployeesPage()
        self.bakeries_page = BakeriesPage()

        #Добавление страниц в стек
        self.stacked_widget.addWidget(self.orders_page)
        self.stacked_widget.addWidget(self.catalog_page)
        self.stacked_widget.addWidget(self.employees_page)
        self.stacked_widget.addWidget(self.bakeries_page)

        #Показываем страницу заказов по умолчанию
        self.stacked_widget.setCurrentWidget(self.orders_page)

    def create_top_navbar(self, layout):
        navbar_widget = QWidget()
        navbar_widget.setStyleSheet("background-color: white; border-bottom: 1px solid #e0e0e0;")
        navbar_layout = QHBoxLayout(navbar_widget)
        navbar_layout.setContentsMargins(20, 10, 20, 10)
        navbar_layout.setSpacing(20)

        self.nav_buttons = {}
        sections = ["Заказы", "Каталог", "Сотрудники", "Филиалы"]

        for section in sections:
            btn = QPushButton(section)
            btn.setFlat(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 11px;
                    color: #666;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    color: #0078d7;
                }
            """)

            btn.clicked.connect(lambda checked, s=section: self.switch_page(s))

            self.nav_buttons[section] = btn
            navbar_layout.addWidget(btn)

        navbar_layout.addStretch()

        #Контейнер для пользователя и кнопки выхода
        user_container = QHBoxLayout()
        user_container.setSpacing(10)

        user_label = QLabel("admin")
        user_label.setStyleSheet(
            "padding: 5px 10px; background-color: #f0f0f0; border-radius: 3px; font-size: 11px;")
        user_container.addWidget(user_label)

        self.logout_btn = QPushButton("Выйти")
        self.logout_btn.setFixedSize(60, 30)
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.logout_btn.clicked.connect(self.logout)
        user_container.addWidget(self.logout_btn)

        navbar_layout.addLayout(user_container)

        layout.addWidget(navbar_widget)

    def switch_page(self, page_name):
        if page_name == "Заказы":
            self.stacked_widget.setCurrentWidget(self.orders_page)
        elif page_name == "Каталог":
            self.stacked_widget.setCurrentWidget(self.catalog_page)
        elif page_name == "Сотрудники":
            self.stacked_widget.setCurrentWidget(self.employees_page)
        elif page_name == "Филиалы":
            self.stacked_widget.setCurrentWidget(self.bakeries_page)

        #Обновляем стиль кнопок
        for section, btn in self.nav_buttons.items():
            if section == page_name:
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 11px;
                        color: #0078d7;
                        font-weight: bold;
                        padding: 5px 10px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 11px;
                        color: #666;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        color: #0078d7;
                    }
                """)

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы действительно хотите выйти из системы?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.close()
            #Показываем окно авторизации
            login_window = LoginScreen()
            login_window.login_successful.connect(self.show_main_after_login)
            login_window.show()

    def show_main_after_login(self):
        self.show()


class MainApplicationManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель менеджера")
        self.setMinimumSize(1200, 600)

        #Центральный виджет со стеком страниц
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #Верхняя панель
        self.create_top_navbar(main_layout)

        #Стек страниц
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        #Все страницы
        self.orders_page = OrdersScreen()

        #Добавление страниц в стек
        self.stacked_widget.addWidget(self.orders_page)

        #Показываем страницу заказов по умолчанию
        self.stacked_widget.setCurrentWidget(self.orders_page)

    def create_top_navbar(self, layout):
        navbar_widget = QWidget()
        navbar_widget.setStyleSheet("background-color: white; border-bottom: 1px solid #e0e0e0;")
        navbar_layout = QHBoxLayout(navbar_widget)
        navbar_layout.setContentsMargins(20, 10, 20, 10)
        navbar_layout.setSpacing(20)

        self.nav_buttons = {}
        sections = ["Заказы"]

        for section in sections:
            btn = QPushButton(section)
            btn.setFlat(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 11px;
                    color: #666;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    color: #0078d7;
                }
            """)

            btn.clicked.connect(lambda checked, s=section: self.switch_page(s))

            self.nav_buttons[section] = btn
            navbar_layout.addWidget(btn)

        navbar_layout.addStretch()

        #Контейнер для пользователя и кнопки выхода
        user_container = QHBoxLayout()
        user_container.setSpacing(10)

        user_label = QLabel("manager")
        user_label.setStyleSheet(
            "padding: 5px 10px; background-color: #f0f0f0; border-radius: 3px; font-size: 11px;")
        user_container.addWidget(user_label)

        self.logout_btn = QPushButton("Выйти")
        self.logout_btn.setFixedSize(60, 30)
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 3px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        self.logout_btn.clicked.connect(self.logout)
        user_container.addWidget(self.logout_btn)

        navbar_layout.addLayout(user_container)

        layout.addWidget(navbar_widget)

    def switch_page(self, page_name):
        if page_name == "Заказы":
            self.stacked_widget.setCurrentWidget(self.orders_page)

        #Обновляем стиль кнопок
        for section, btn in self.nav_buttons.items():
            if section == page_name:
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 11px;
                        color: #0078d7;
                        font-weight: bold;
                        padding: 5px 10px;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        font-size: 11px;
                        color: #666;
                        padding: 5px 10px;
                    }
                    QPushButton:hover {
                        color: #0078d7;
                    }
                """)

    def logout(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы действительно хотите выйти из системы?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.close()
            #Показываем окно авторизации
            login_window = LoginScreen()
            login_window.login_successful.connect(self.show_main_after_login)
            login_window.show()

    def show_main_after_login(self):
        self.show()


class ApplicationController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')

        self.login_window = LoginScreen()
        self.login_window.login_successful.connect(self.show_main_window)

        self.main_window = None

    def show_main_window(self):
        if session_access == 1:
            self.main_window = MainApplication()
        elif session_access == 2:
            self.main_window = MainApplicationManager()
        self.main_window.show()

    def run(self):
        self.login_window.show()
        return self.app.exec()


def main():
    controller = ApplicationController()
    sys.exit(controller.run())


if __name__ == "__main__":
    main()