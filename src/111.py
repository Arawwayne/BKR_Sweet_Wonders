import sys
import csv
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QFrame, QDialog, QGridLayout, QComboBox, QMessageBox,
    QDialogButtonBox, QGroupBox, QStackedWidget, QTabWidget, QListWidget,
    QListWidgetItem, QTextEdit, QDateEdit, QSpinBox, QDoubleSpinBox,
    QCheckBox, QRadioButton, QButtonGroup, QSplitter, QTreeWidget,
    QTreeWidgetItem, QProgressBar, QSlider, QDial, QFileDialog, QScrollArea, QTextEdit
)
from PySide6.QtCore import Qt, QSize, Signal, QDate, QTimer
from PySide6.QtGui import QFont, QColor, QIcon, QPixmap, QPainter, QPen
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
import random
from datetime import datetime, timedelta

from CRUD import *


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
        main_layout.setSpacing(15)

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
                padding: 8px 12px;
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
                padding: 8px 12px;
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

        if login == "":
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            self.login_input.setFocus()
            return

        if password == "":
            QMessageBox.warning(self, "Ошибка", "Введите пароль")
            self.password_input.setFocus()
            return

        #Учётные данные для входа
        valid_credentials = {
            "admin": "admin123",
            "1": "1"
        }

        if login in valid_credentials and valid_credentials[login] == password:
            self.login_successful.emit()
            self.close()
        else:
            QMessageBox.critical(
                self,
                "Ошибка авторизации",
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
        self.setWindowTitle(f"Заказ: {order_data['order_number']}")
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
        title_label = QLabel(f"Заказ: {self.order_data['order_number']}")
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
        info_layout.addWidget(QLabel("Имя пользователя:"), row, 0)
        info_layout.addWidget(QLabel(self.order_data['username']), row, 1)

        row += 1
        info_layout.addWidget(QLabel("Телефон пользователя:"), row, 0)
        info_layout.addWidget(QLabel(self.order_data['phone']), row, 1)

        row += 1
        info_layout.addWidget(QLabel("Дата создания заказа:"), row, 0)
        info_layout.addWidget(QLabel(self.order_data['created_date']), row, 1)

        row += 1
        info_layout.addWidget(QLabel("Дата выполнения:"), row, 0)
        info_layout.addWidget(QLabel(self.order_data['completed_date']), row, 1)

        row = 0
        info_layout.addWidget(QLabel("Наименование заведения:"), row, 2)
        info_layout.addWidget(QLabel(self.order_data['establishment']), row, 3)

        row += 1
        info_layout.addWidget(QLabel("Адрес заведения:"), row, 2)
        info_layout.addWidget(QLabel(self.order_data['address']), row, 3)

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

        #Сумма заказа
        total_frame = QFrame()
        total_frame.setFrameShape(QFrame.StyledPanel)
        total_frame.setStyleSheet("background-color: #f8f9fa; padding: 10px; border-radius: 5px;")
        total_layout = QHBoxLayout(total_frame)

        total_label = QLabel("Сумма заказа:")
        total_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        total_value = QLabel(self.order_data['total'])
        total_value.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d7;")

        total_layout.addWidget(total_label)
        total_layout.addWidget(total_value)
        total_layout.addStretch()

        layout.addWidget(total_frame)

        #Статус и кнопки
        status_layout = QHBoxLayout()

        status_label = QLabel("Статус:")
        status_label.setStyleSheet("font-size: 13px; font-weight: bold;")

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Открыт", "В работе", "Готов", "Завершён", "Отменён"])
        self.status_combo.setCurrentText(self.order_data['status'])
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
        items = self.order_data.get('items', [])
        self.items_table.setRowCount(len(items))

        for row, item in enumerate(items):
            self.items_table.setItem(row, 0, QTableWidgetItem(item['name']))

            quantity_item = QTableWidgetItem(str(item['quantity']))
            quantity_item.setTextAlignment(Qt.AlignCenter)
            self.items_table.setItem(row, 1, quantity_item)

            total_item = QTableWidgetItem(f"{item['total']:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.items_table.setItem(row, 2, total_item)

    def get_updated_status(self):
        return self.status_combo.currentText()


class OrdersScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1200, 600)
        self.all_orders_data = {
            "00001": {
                'order_number': '00001',
                'username': 'Васян',
                'phone': '+79823145521',
                'created_date': '09.09.2026',
                'completed_date': '11:30 12.09.2026',
                'establishment': 'Мягкая булка 17',
                'address': 'С. Молочное Ул. Попова 17',
                'total': '89.00',
                'status': 'Открыт',
                'items': [{'name': 'Синнабон корейский', 'quantity': 1, 'total': 89.00}]
            },
            "00002": {
                'order_number': '00002',
                'username': 'Мария',
                'phone': '+79229281777',
                'created_date': '09.09.2026',
                'completed_date': '17:30 10.09.2026',
                'establishment': 'Мягкая булка 17',
                'address': 'С. Молочное Ул. Попова 17',
                'total': '1000.00',
                'status': 'В работе',
                'items': [
                    {'name': 'Синнабон корейский', 'quantity': 2, 'total': 240.00},
                    {'name': 'Кремобон карамельный', 'quantity': 1, 'total': 160.00}
                ]
            },
            "00003": {
                'order_number': '00003',
                'username': 'Иван Петров',
                'phone': '+79991234567',
                'created_date': '10.09.2026',
                'completed_date': '15:30 10.09.2026',
                'establishment': 'Мягкая булка 17',
                'address': 'С. Молочное Ул. Попова 17',
                'total': '450.00',
                'status': 'Готов',
                'items': [{'name': 'Пирожное', 'quantity': 3, 'total': 450.00}]
            },
            "00004": {
                'order_number': '00004',
                'username': 'Анна Смирнова',
                'phone': '+79876543210',
                'created_date': '08.09.2026',
                'completed_date': '12:00 09.09.2026',
                'establishment': 'Мягкая булка 17',
                'address': 'С. Молочное Ул. Попова 17',
                'total': '1200.00',
                'status': 'Завершён',
                'items': [{'name': 'Торт', 'quantity': 1, 'total': 1200.00}]
            },
            "00005": {
                'order_number': '00005',
                'username': 'Сергей Козлов',
                'phone': '+79112223344',
                'created_date': '07.09.2026',
                'completed_date': '—',
                'establishment': 'Мягкая булка 17',
                'address': 'С. Молочное Ул. Попова 17',
                'total': '300.00',
                'status': 'Отменён',
                'items': [{'name': 'Кофе', 'quantity': 2, 'total': 300.00}]
            }
        }

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
        self.filter_orders("Все заказы")

        self.table.cellDoubleClicked.connect(self.on_order_double_clicked)

    def create_status_bar(self, layout):
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)

        self.status_buttons = {}
        statuses = ["Все заказы", "Открытые", "В работе", "Готовые", "Завершённые", "Отменённые"]

        self.status_mapping = {
            "Все заказы": None,
            "Открытые": "Открыт",
            "В работе": "В работе",
            "Готовые": "Готов",
            "Завершённые": "Завершён",
            "Отменённые": "Отменён"
        }

        for status in statuses:
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
        self.filter_orders(status)

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

    def filter_orders(self, status):
        filter_status = self.status_mapping.get(status)

        if filter_status is None:
            filtered_orders = list(self.all_orders_data.values())
        else:
            filtered_orders = [
                order for order in self.all_orders_data.values()
                if order['status'] == filter_status
            ]

        self.update_table(filtered_orders)

    def update_table(self, orders):
        self.table.setRowCount(0)

        display_data = []
        for order in orders:
            display_data.append([
                order['order_number'],
                order['username'],
                order['total'],
                order['phone'],
                order['created_date'],
                order['completed_date'],
                order['status']
            ])

        display_data.sort(key=lambda x: x[0], reverse=True)

        self.table.setRowCount(len(display_data))

        for row, order_data in enumerate(display_data):
            num_item = QTableWidgetItem(order_data[0])
            num_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, num_item)

            for col, value in enumerate(order_data[1:]):
                item = QTableWidgetItem(str(value))

                if col in [1, 2, 3, 4]:
                    item.setTextAlignment(Qt.AlignCenter)

                if col == 5:
                    item.setTextAlignment(Qt.AlignCenter)
                    self.color_status_item(item, value)

                self.table.setItem(row, col + 1, item)

    def color_status_item(self, item, status):
        colors = {
            "Открыт": ("#28a745", "#e8f5e9"),
            "В работе": ("#ff8c00", "#fff3e0"),
            "Готов": ("#0078d7", "#e6f2fa"),
            "Завершён": ("#6c757d", "#f8f9fa"),
            "Отменён": ("#dc3545", "#f8d7da")
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
            "№ Заказа", "Имя пользователя", "Сумма заказа",
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
        order_number = self.table.item(row, 0).text()
        if order_number in self.all_orders_data:
            dialog = OrderDetailDialog(self.all_orders_data[order_number], self)
            if dialog.exec() == QDialog.Accepted:
                new_status = dialog.get_updated_status()
                self.update_order_status(order_number, new_status)

    def update_order_status(self, order_number, new_status):
        if order_number in self.all_orders_data:
            self.all_orders_data[order_number]['status'] = new_status
            self.filter_orders(self.current_filter)

    def search_orders(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.filter_orders(self.current_filter)
            return

        filter_status = self.status_mapping.get(self.current_filter)
        if filter_status is None:
            current_orders = list(self.all_orders_data.values())
        else:
            current_orders = [
                order for order in self.all_orders_data.values()
                if order['status'] == filter_status
            ]

        #Поиск по тексту
        filtered_orders = []
        for order in current_orders:
            if (search_text in order['order_number'].lower() or  #Поиск по номеру
                    search_text in order['username'].lower() or  #Поиск по имени
                    search_text in order['phone'].lower()):  #Поиск по телефону
                filtered_orders.append(order)

        if filtered_orders:
            self.update_table(filtered_orders)
        else:
            QMessageBox.information(self, "Поиск", "Ничего не найдено")
            self.filter_orders(self.current_filter)


class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить изделие")
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
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        #Заголовок
        title = QLabel("Добавление изделия")
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
        self.category_combo.addItems(["Синнабоны", "Кремобоны", "Пирожные", "Торты", "Напитки"])
        self.category_combo.setEditable(True)
        form_layout.addWidget(self.category_combo, 1, 1)

        #Количество на складе
        form_layout.addWidget(QLabel("Количество:"), 1, 2)
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 10000)
        self.quantity_spin.setSuffix(" шт")
        form_layout.addWidget(self.quantity_spin, 1, 3)

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
        # return {
        #     'name': self.name_input.text().strip(),
        #     'category': self.category_combo.currentText(),
        #     'cost_price': self.cost_price.value(),
        #     'selling_price': self.selling_price.value(),
        #     'quantity': self.quantity_spin.value(),
        #     'description': self.desc_input.text().strip(),
        #     'ingredients': self.ingredients_input.text().strip(),
        #     'calories': self.calories_spin.value(),
        #     'fats': self.fats_spin.value(),
        #     'proteins': self.proteins_spin.value(),
        #     'carbs': self.carbs_spin.value(),
        #     'image_path': getattr(self, 'selected_image_path', None)
        # }
    
        return {
            #'article': self.
            "name": self.name_input.text().strip(),
            "category_id": self.category_combo.currentText(),
            "sale_price": self.selling_price.value(),
            "cost_price": self.cost_price.value(),
            "composition": self.ingredients_input.text().strip(),
            "description": self.desc_input.text().strip(),
            "calories": self.calories_spin.value(),
            "protein": self.proteins_spin.value(),
            "fat": self.fats_spin.value(),
            "carbs": self.carbs_spin.value(),
            "weight": self.quantity_spin.value(), # тк веса в админке нету, а количества нет на сайте, пока будет так, что количество == вес
            "is_visible": True,
            "id": 1,
            "image_url": getattr(self, 'selected_image_path', None)
        }



class AddCategoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить категорию")
        self.setMinimumSize(400, 300)
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

        layout.addWidget(button_box)

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите наименование категории")
            self.name_input.setFocus()
            return

        self.accept()

    def get_category_data(self):
        return {
            'name': self.name_input.text().strip(),
            'order': self.order_spin.value()
        }


class ProductViewDialog(QDialog):
    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        self.product_data = product_data
        self.selected_image_path = None
        self.setWindowTitle(f"Просмотр изделия: {product_data[1] if len(product_data) > 1 else ''}")
        self.setMinimumSize(800, 600)
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
            QCheckBox::indicator:checked {
                border: 1px solid #0078d7;
                background-color: #0078d7;
                border-radius: 3px;
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
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        #Заголовок
        product_name = self.product_data[1] if len(self.product_data) > 1 else ""
        title_label = QLabel(f"Изделие: {product_name}")
        title_label.setProperty("heading", True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title_label)

        #Информация об изделии
        info_group = QGroupBox("Информация об изделии")
        info_layout = QGridLayout(info_group)
        info_layout.setVerticalSpacing(12)
        info_layout.setHorizontalSpacing(20)
        info_layout.setContentsMargins(15, 20, 15, 15)

        #Артикул
        info_layout.addWidget(QLabel("Артикул:"), 0, 0)
        article_value = self.product_data[0] if len(self.product_data) > 0 else ""
        article_label = QLabel(f"<b>{article_value}</b>")
        article_label.setStyleSheet("color: #0078d7; font-size: 13px;")
        info_layout.addWidget(article_label, 0, 1)

        #Наименование
        info_layout.addWidget(QLabel("Наименование:"), 1, 0)
        self.name_edit = QLineEdit(product_name)
        self.name_edit.setPlaceholderText("Введите наименование изделия")
        info_layout.addWidget(self.name_edit, 1, 1, 1, 3)

        #Категория
        info_layout.addWidget(QLabel("Категория:"), 2, 0)
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Синнабоны", "Кремобоны", "Пирожные", "Торты", "Напитки"])
        self.category_combo.setEditable(True)
        if len(self.product_data) > 2:
            current_category = self.product_data[2]
            index = self.category_combo.findText(current_category)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
            else:
                self.category_combo.setCurrentText(current_category)
        info_layout.addWidget(self.category_combo, 2, 1)

        #Себестоимость
        info_layout.addWidget(QLabel("Себестоимость:"), 3, 0)
        self.cost_price = QDoubleSpinBox()
        self.cost_price.setRange(0, 100000)
        self.cost_price.setPrefix("₽ ")
        self.cost_price.setDecimals(2)
        self.cost_price.setSingleStep(10)
        if len(self.product_data) > 3:
            try:
                self.cost_price.setValue(float(self.product_data[3]) if self.product_data[3] else 0)
            except (ValueError, TypeError):
                self.cost_price.setValue(0)
        info_layout.addWidget(self.cost_price, 3, 1)

        #Цена
        info_layout.addWidget(QLabel("Цена:"), 3, 2)
        self.selling_price = QDoubleSpinBox()
        self.selling_price.setRange(0, 100000)
        self.selling_price.setPrefix("₽ ")
        self.selling_price.setDecimals(2)
        self.selling_price.setSingleStep(10)
        if len(self.product_data) > 4:
            try:
                self.selling_price.setValue(float(self.product_data[4]) if self.product_data[4] else 0)
            except (ValueError, TypeError):
                self.selling_price.setValue(0)
        info_layout.addWidget(self.selling_price, 3, 3)

        #Количество на складе
        info_layout.addWidget(QLabel("Количество:"), 2, 2)
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(0, 10000)
        self.quantity_spin.setSuffix(" шт")
        if len(self.product_data) > 6:
            try:
                quantity = self.product_data[6]
                quantity_value = int(quantity) if quantity else 0
                self.quantity_spin.setValue(quantity_value)
            except (ValueError, TypeError):
                self.quantity_spin.setValue(0)
        info_layout.addWidget(self.quantity_spin, 2, 3)

        #Описание
        info_layout.addWidget(QLabel("Описание:"), 4, 0)
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Введите описание изделия")
        if len(self.product_data) > 7:
            self.desc_input.setText(str(self.product_data[7]) if self.product_data[7] else "")
        info_layout.addWidget(self.desc_input, 4, 1, 1, 3)

        #Состав
        info_layout.addWidget(QLabel("Состав:"), 5, 0)
        self.ingredients_input = QLineEdit()
        self.ingredients_input.setPlaceholderText("Введите состав изделия")
        if len(self.product_data) > 8:
            self.ingredients_input.setText(str(self.product_data[8]) if self.product_data[8] else "")
        info_layout.addWidget(self.ingredients_input, 5, 1, 1, 3)

        #Энергетическая ценность
        info_layout.addWidget(QLabel("Энергетическая ценность:"), 6, 0)
        self.calories_spin = QSpinBox()
        self.calories_spin.setRange(0, 10000)
        self.calories_spin.setSuffix(" ккал")
        if len(self.product_data) > 9:
            try:
                self.calories_spin.setValue(int(self.product_data[9]) if self.product_data[9] else 0)
            except (ValueError, TypeError):
                self.calories_spin.setValue(0)
        info_layout.addWidget(self.calories_spin, 6, 1)

        #Жиры
        info_layout.addWidget(QLabel("Жиры:"), 6, 2)
        self.fats_spin = QDoubleSpinBox()
        self.fats_spin.setRange(0, 1000)
        self.fats_spin.setSuffix(" г")
        self.fats_spin.setDecimals(1)
        if len(self.product_data) > 10:
            try:
                self.fats_spin.setValue(float(self.product_data[10]) if self.product_data[10] else 0)
            except (ValueError, TypeError):
                self.fats_spin.setValue(0)
        info_layout.addWidget(self.fats_spin, 6, 3)

        # Белки
        info_layout.addWidget(QLabel("Белки:"), 7, 0)
        self.proteins_spin = QDoubleSpinBox()
        self.proteins_spin.setRange(0, 1000)
        self.proteins_spin.setSuffix(" г")
        self.proteins_spin.setDecimals(1)
        if len(self.product_data) > 11:
            try:
                self.proteins_spin.setValue(float(self.product_data[11]) if self.product_data[11] else 0)
            except (ValueError, TypeError):
                self.proteins_spin.setValue(0)
        info_layout.addWidget(self.proteins_spin, 7, 1)

        #Углеводы
        info_layout.addWidget(QLabel("Углеводы:"), 7, 2)
        self.carbs_spin = QDoubleSpinBox()
        self.carbs_spin.setRange(0, 1000)
        self.carbs_spin.setSuffix(" г")
        self.carbs_spin.setDecimals(1)
        if len(self.product_data) > 12:
            try:
                self.carbs_spin.setValue(float(self.product_data[12]) if self.product_data[12] else 0)
            except (ValueError, TypeError):
                self.carbs_spin.setValue(0)
        info_layout.addWidget(self.carbs_spin, 7, 3)

        #Отображение
        self.show_on_display = QCheckBox("Отображать изделие")
        self.show_on_display.setChecked(True)
        if len(self.product_data) > 5:
            try:
                self.show_on_display.setChecked(bool(self.product_data[5]))
            except (ValueError, TypeError):
                pass
        info_layout.addWidget(self.show_on_display, 8, 0, 1, 2)

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
        info_layout.addWidget(self.pic_button, 9, 0, 1, 2)

        #Метка для отображения пути к файлу
        self.image_path_label = QLabel("Файл не выбран")
        self.image_path_label.setStyleSheet("color: #666; font-size: 11px; padding: 5px;")
        info_layout.addWidget(self.image_path_label, 9, 2, 1, 2)

        layout.addWidget(info_group)

        #Кнопки
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setText("Сохранить")
        ok_button.setMinimumWidth(120)
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
        cancel_button.setMinimumWidth(120)
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

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(button_box)
        layout.addLayout(button_layout)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif);;Все файлы (*.*)"
        )

        if file_path:
            self.selected_image_path = file_path
            self.image_path_label.setText(f"✓ {file_path}")
            self.image_path_label.setStyleSheet("color: #28a745; font-size: 11px; padding: 5px;")
            print(f"Изображение загружено: {file_path}")

    def get_updated_data(self):
        return {
            'article': self.product_data[0] if len(self.product_data) > 0 else '',
            'name': self.name_edit.text().strip(),
            'category': self.category_combo.currentText(),
            'cost_price': self.cost_price.value(),
            'selling_price': self.selling_price.value(),
            'show_on_display': self.show_on_display.isChecked(),
            'quantity': self.quantity_spin.value(),
            'description': self.desc_input.text(),
            'ingredients': self.ingredients_input.text(),
            'calories': self.calories_spin.value(),
            'fats': self.fats_spin.value(),
            'proteins': self.proteins_spin.value(),
            'carbs': self.carbs_spin.value(),
            'image_path': self.selected_image_path
        }

    def accept(self):
        #Валидация
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Наименование изделия не может быть пустым!")
            return

        if self.selling_price.value() <= 0:
            reply = QMessageBox.question(
                self,
                "Подтверждение",
                "Цена равна 0. Продолжить?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        super().accept()

class CategoryViewDialog(QDialog):
    def __init__(self, category_data, parent=None):
        super().__init__(parent)
        self.category_data = category_data
        self.setWindowTitle(f"Просмотр категории: {category_data[0]}")
        self.setMinimumSize(500, 350)
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
            QCheckBox::indicator:checked {
                border: 1px solid #0078d7;
                background-color: #0078d7;
                border-radius: 3px;
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
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        #Заголовок
        title_label = QLabel(f"Категория: {self.category_data[0]}")
        title_label.setProperty("heading", True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title_label)

        #Информация о категории
        info_group = QGroupBox("Информация о категории")
        info_layout = QGridLayout(info_group)
        info_layout.setVerticalSpacing(12)
        info_layout.setHorizontalSpacing(20)

        #Наименование
        info_layout.addWidget(QLabel("Наименование:"), 0, 0)
        info_layout.addWidget(QLineEdit(f"{self.category_data[0]}"), 0, 1)

        #Порядок
        info_layout.addWidget(QLabel("Порядок:"), 1, 0)
        self.order_spin = QSpinBox()
        self.order_spin.setRange(1, 100)

        try:
            if len(self.category_data) > 1 and self.category_data[1] is not None:
                order_value = int(self.category_data[1])
            else:
                order_value = 1
        except (ValueError, TypeError):
            order_value = 1
            print(f"Ошибка преобразования значения порядка: {self.category_data[1]}")

        self.order_spin.setValue(order_value)
        self.order_spin.setSuffix("")
        info_layout.addWidget(self.order_spin, 1, 1)

        #Отображение
        self.show_on_display = QCheckBox("Отображать категорию")
        self.show_on_display.setChecked(True)
        info_layout.addWidget(self.show_on_display, 8, 0)

        layout.addWidget(info_group)

        #Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.save_button = QPushButton("Сохранить")
        self.save_button.setObjectName("saveButton")
        self.save_button.setStyleSheet("""
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

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)
        self.cancel_button.setStyleSheet("""
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

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)


class CatalogPage(QWidget):
    def __init__(self):
        super().__init__()
        #Данные для изделий
        self.all_catalog_data = self.dict_to_list(get_products())
        
        # {
        #     "name": "Шоколадный пончик",
        #     "category_id": 1,
        #     "sale_price": 100.0,
        #     "cost_price": 30.0,
        #     "composition": "Тесто, Мука, Молоко, Яйца, Глазурь, Масло",
        #     "description": "Пончик в шоколадной глазури, покрытый топингом.",
        #     "calories": 230,
        #     "protein": 3.0,
        #     "fat": 45.0,
        #     "carbs": 21.0,
        #     "weight": 100,
        #     "is_visible": True,
        #     "id": 1,
        #     "image_url": None
        # }
        # self.all_catalog_data = self.dict_to_list(self.all_catalog_data)
        

        # self.all_catalog_data = [
        #     ["001", "Синнабон классический", "Синнабоны", "120.00", "100.00", "синнабон, классический, корица", "100"], ]

        #     ["002", "Синнабон с шоколадом", "Синнабоны", "140.00", "110.00", "синнабон, шоколад", "100"],
        #     ["003", "Синнабон карамельный", "Синнабоны", "135.00", "105.00", "синнабон, карамель", "100"],
        #     ["004", "Кремобон ванильный", "Кремобоны", "160.00", "130.00", "кремобон, ваниль", "100"],
        #     ["005", "Кремобон шоколадный", "Кремобоны", "170.00", "150.00", "кремобон, шоколад", "100"],
        #     ["006", "Кремобон карамельный", "Кремобоны", "165.00", "140.00", "кремобон, карамель", "100"],
        #     ["007", "Пирожное корзиночка", "Пирожные", "80.00", "60.00", "пирожное, корзиночка", "100"],
        #     ["008", "Эклер ванильный", "Пирожные", "90.00", "70.00", "эклер, ваниль", "100"],
        #     ["009", "Профитроли", "Пирожные", "75.00", "40.00", "профитроли, заварные", "100"],
        #     ["010", "Медовый торт", "Торты", "450.00", "400.00", "торт, медовый", "100"],
        #     ["011", "Наполеон", "Торты", "500.00", "410.00", "торт, наполеон", "100"],
        #     ["012", "Капучино", "Напитки", "120.00", "80.00", "кофе, капучино", "100"],
        #     ["013", "Латте", "Напитки", "130.00", "100.00", "кофе, латте", "100"],
        #     ["014", "Чай черный", "Напитки", "50.00", "31.00", "чай, черный", "100"],
        # ]

        #Данные для категорий
        self.categories_data = [
            ["Синнабоны", "1"],
            ["Кремобоны", "2"],
            ["Пирожные", "3"],
            ["Торты", "4"],
            ["Напитки", "5"],
            ["Десерты", "6"],
            ["Выпечка", "7"],
        ]

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

    def dict_to_list(self, dict):
        # ["001", "Синнабон классический", "Синнабоны", "120.00", "100.00", "синнабон, классический, корица", "100"],
        data_list = []
         # Если передан JSON-строкой, парсим её
        data = dict

        # Получаем список продуктов
        products = data.get("products", [])
        
        # Создаём многоуровневый список
        
        for product in products:
            # Создаём список для каждого продукта
            product_data = [
                product.get("id", 0),
                product.get("name", ""),
                product.get("category_id", ""),
                product.get("cost_price", 0.0),
                product.get("sale_price", 0.0),
                product.get("composition", ""),
                product.get("description", ""),
                product.get("calories", 0),
                product.get("protein", 0.0),
                product.get("fat", 0.0),
                product.get("carbs", 0.0),
                product.get("weight", 0),
                product.get("is_visible", True),
                product.get("image_url", "")
            ]
            data_list.append(product_data)

        return data_list

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

        self.populate_products_table()
        layout.addWidget(self.products_table)

        return page

    def on_product_double_clicked(self, row, column):
        product_data = []
        for col in range(self.products_table.columnCount()):
            product_data.append(self.products_table.item(row, col).text())

        if len(self.all_catalog_data[row]) > 5:
            product_data.append(self.all_catalog_data[row][5])  # теги
        if len(self.all_catalog_data[row]) > 6:
            product_data.append(self.all_catalog_data[row][6])  # количество

        dialog = ProductViewDialog(product_data, self)
        dialog.exec()

    def populate_products_table(self, data=None):
        if data is None:
            data = self.all_catalog_data

        self.products_table.setRowCount(len(data))

        for row, item_data in enumerate(data):
            for col, value in enumerate(item_data[:5]):
                item = QTableWidgetItem(str(value))

                #if col == 0 or col == 3 or col == 4:
                item.setTextAlignment(Qt.AlignCenter)

                self.products_table.setItem(row, col, item)

    def search_products(self):
        search_text = self.products_search.text().lower()
        if not search_text:
            self.populate_products_table()
            return

        filtered_data = []
        for item in self.all_catalog_data:
            if (search_text in item[0].lower() or  #Поиск по артикулу
                search_text in item[1].lower() or  #Поиск по названию
                search_text in item[2].lower()):   #Поиск по категории
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
            product_data = dialog.get_product_data()
            self.add_product(product_data)

    def add_product(self, data):
        new_article = str(int(self.all_catalog_data[-1][0]) + 1).zfill(3)

        new_product = [
            new_article,
            data['name'],
            data['category'],
            f"{data['cost_price']:.2f}",
            f"{data['selling_price']:.2f}",
            data['tags'],
            str(data['quantity'])
        ]
        self.all_catalog_data.append(new_product)
        self.populate_products_table()
        QMessageBox.information(self, "Успешно", f"Изделие '{data['name']}' добавлено!")

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
        self.categories_table.setColumnCount(2)
        self.categories_table.setHorizontalHeaderLabels([
            "Наименование категории изделий", "Порядок категории"
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

        self.populate_categories_table()

        layout.addWidget(self.categories_table)

        return page

    def on_category_double_clicked(self, row, column):
        category_name = self.categories_table.item(row, 0).text()
        category_order = self.categories_table.item(row, 1).text()

        category_data = [category_name, category_order]
        dialog = CategoryViewDialog(category_data, self)
        dialog.exec()

    def populate_categories_table(self, data=None):
        if data is None:
            data = self.categories_data

        self.categories_table.setRowCount(len(data))

        for row, cat_data in enumerate(data):
            for col, value in enumerate(cat_data):
                item = QTableWidgetItem(str(value))

                if col == 1:
                    item.setTextAlignment(Qt.AlignCenter)

                self.categories_table.setItem(row, col, item)

    def search_categories(self):
        search_text = self.categories_search.text().lower()
        if not search_text:
            self.populate_categories_table()
            return

        filtered_data = []
        for cat in self.categories_data:
            if search_text in cat[0].lower():
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
        dialog = AddCategoryDialog(self)
        if dialog.exec() == QDialog.Accepted:
            category_data = dialog.get_category_data()
            self.add_category(category_data)

    def add_category(self, data):
        new_category = [data['name'], str(data['order'])]
        self.categories_data.append(new_category)
        self.populate_categories_table()
        QMessageBox.information(self, "Успешно", f"Категория '{data['name']}' добавлена!")


class AddEmployeeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        title = QLabel("Добавление сотрудника")
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
        form_layout.addWidget(self.phone_input, 5, 1)

        #Почта
        form_layout.addWidget(QLabel("Почта:"), 6, 0)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Введите корпоративную почту сотрудника")
        form_layout.addWidget(self.email_input, 6, 1)

        #Должность
        form_layout.addWidget(QLabel("Должность:"), 7, 0)
        self.position_combo = QComboBox()
        self.position_combo.addItems(["Администратор", "Менеджер"])
        form_layout.addWidget(self.position_combo, 7, 1)

        #Филиал
        form_layout.addWidget(QLabel("Филиал:"), 8, 0)
        self.branch_combo = QComboBox()
        self.branch_combo.addItems(["Европейский", "Звукоуловитель", "Октябрьский", "Волжский", "Дальний", "Нагорский", "Дульсе"])
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

        if not self.email_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите email сотрудника")
            self.email_input.setFocus()
            return

        self.accept()

    def get_employee_data(self):
        return {
            'lastname': self.lastname_input.text().strip(),
            'firstname': self.firstname_input.text().strip(),
            'patronymic': self.patronymic_input.text().strip(),
            'login': self.login_input.text().strip(),
            'password': self.password_input.text(),
            'phone': self.phone_input.text().strip(),
            'email': self.email_input.text().strip(),
            'position': self.position_combo.currentText(),
            'branch': self.branch_combo.currentText()
        }


class EmployeeDetailDialog(QDialog):
    employee_deleted = Signal(int)

    def __init__(self, employee_data, parent=None):
        super().__init__(parent)
        self.employee_data = employee_data
        self.employee_id = employee_data[0] if employee_data else 0
        self.setWindowTitle(f"Сотрудник: {employee_data[1]} {employee_data[2]}")
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
        title_label = QLabel(f"Сотрудник: {self.employee_data[1]} {self.employee_data[2]} {self.employee_data[3]}")
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
        id_label = QLabel(f"<b>{self.employee_data[0]}</b>")
        info_layout.addWidget(id_label, 0, 1)

        #Фамилия
        info_layout.addWidget(QLabel("Фамилия:"), 1, 0)
        self.lastname_input = QLineEdit(self.employee_data[1])
        info_layout.addWidget(self.lastname_input, 1, 1)

        #Имя
        info_layout.addWidget(QLabel("Имя:"), 2, 0)
        self.firstname_input = QLineEdit(self.employee_data[2])
        info_layout.addWidget(self.firstname_input, 2, 1)

        #Отчество
        info_layout.addWidget(QLabel("Отчество:"), 3, 0)
        self.patronymic_input = QLineEdit(self.employee_data[3])
        info_layout.addWidget(self.patronymic_input, 3, 1)

        #Логин
        info_layout.addWidget(QLabel("Логин:"), 4, 0)
        self.login_input = QLineEdit(self.employee_data[4] if len(self.employee_data) > 4 else "")
        info_layout.addWidget(self.login_input, 4, 1)

        #Телефон
        info_layout.addWidget(QLabel("Телефон:"), 5, 0)
        self.phone_input = QLineEdit(self.employee_data[4] if len(self.employee_data) > 4 else "")
        info_layout.addWidget(self.phone_input, 5, 1)

        #Email
        info_layout.addWidget(QLabel("Email:"), 6, 0)
        self.email_input = QLineEdit(self.employee_data[5] if len(self.employee_data) > 5 else "")
        info_layout.addWidget(self.email_input, 6, 1)

        #Должность
        info_layout.addWidget(QLabel("Должность:"), 7, 0)
        self.position_combo = QComboBox()
        self.position_combo.addItems(["Администратор", "Менеджер"])
        self.position_combo.setCurrentText(self.employee_data[6] if len(self.employee_data) > 6 else "Менеджер")
        info_layout.addWidget(self.position_combo, 7, 1)

        #Филиал
        info_layout.addWidget(QLabel("Филиал:"), 8, 0)
        self.branch_combo = QComboBox()
        self.branch_combo.addItems(
            ["Европейский", "Звукоуловитель", "Октябрьский", "Волжский", "Дальний", "Нагорский", "Дульсе"])
        self.branch_combo.setCurrentText(self.employee_data[7] if len(self.employee_data) > 7 else "Европейский")
        info_layout.addWidget(self.branch_combo, 8, 1)

        #Статус сотрудника
        info_layout.addWidget(QLabel("Статус:"), 9, 0)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Работает", "В отпуске", "На больничном", "Уволен"])
        self.status_combo.setCurrentText(self.employee_data[8] if len(self.employee_data) > 8 else "Работает")
        info_layout.addWidget(self.status_combo, 9, 1)

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

        if not self.email_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите email сотрудника")
            self.email_input.setFocus()
            return

        self.accept()

    def delete_employee(self):
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы действительно хотите удалить сотрудника {self.employee_data[1]} {self.employee_data[2]}?\n\nЭто действие нельзя отменить.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.employee_deleted.emit(int(self.employee_id))
            self.reject()

    def get_updated_data(self):
        return {
            'id': self.employee_id,
            'lastname': self.lastname_input.text().strip(),
            'firstname': self.firstname_input.text().strip(),
            'patronymic': self.patronymic_input.text().strip(),
            'login': self.login_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'email': self.email_input.text().strip(),
            'position': self.position_combo.currentText(),
            'branch': self.branch_combo.currentText(),
            'status': self.status_combo.currentText()
        }


class EmployeesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.all_employees_data = [
            ["1", "Иванов", "Иван", "Иванович", "+7(999)123-45-67", "ivanov@example.com", "Администратор",
             "Европейский", "Работает"],
            ["2", "Петрова", "Мария", "Сергеевна", "+7(999)234-56-78", "petrova@example.com", "Администратор",
             "Звукоуловитель", "Работает"],
            ["3", "Сидоров", "Алексей", "Петрович", "+7(999)345-67-89", "sidorov@example.com", "Менеджер",
             "Октябрьский", "Работает"],
            ["4", "Козлова", "Елена", "Андреевна", "+7(999)456-78-90", "kozlova@example.com", "Менеджер", "Октябрьский",
             "В отпуске"],
            ["5", "Морозов", "Дмитрий", "Николаевич", "+7(999)567-89-01", "morozov@example.com", "Менеджер", "Волжский",
             "Работает"],
            ["6", "Волкова", "Анна", "Владимировна", "+7(999)678-90-12", "volkova@example.com", "Менеджер", "Дальний",
             "На больничном"]
        ]
        self.next_id = len(self.all_employees_data) + 1

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
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Фамилия", "Имя", "Отчество", "Телефон", "Корпоративная почта", "Должность", "Филиал", "Статус"
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

    def populate_employees(self, data=None):
        if data is None:
            data = self.all_employees_data

        self.table.setRowCount(len(data))

        for row, emp_data in enumerate(data):
            for col, value in enumerate(emp_data):
                item = QTableWidgetItem(str(value))

                if col == 0 or col == 8:
                    item.setTextAlignment(Qt.AlignCenter)

                if col == 8:  # Статус
                    if value == "Работает":
                        item.setForeground(QColor("#28a745"))
                        item.setBackground(QColor("#e8f5e9"))
                    elif value == "В отпуске":
                        item.setForeground(QColor("#ff8c00"))
                        item.setBackground(QColor("#fff3e0"))
                    elif value == "На больничном":
                        item.setForeground(QColor("#dc3545"))
                        item.setBackground(QColor("#f8d7da"))
                    elif value == "Уволен":
                        item.setForeground(QColor("#6c757d"))
                        item.setBackground(QColor("#f8f9fa"))

                self.table.setItem(row, col, item)

    def search_employees(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.filter_employees_by_status(self.status_filter.currentText())
            return

        filtered_data = []
        for emp in self.all_employees_data:
            full_name = f"{emp[1]} {emp[2]} {emp[3]}".lower()
            if (search_text in full_name or  # Поиск по ФИО
                    search_text in emp[4].lower() or  # Поиск по телефону
                    search_text in emp[6].lower()):  # Поиск по должности
                filtered_data.append(emp)

        if filtered_data:
            self.populate_employees(filtered_data)
        else:
            QMessageBox.information(self, "Поиск", "Ничего не найдено")

    def clear_search(self):
        self.search_input.clear()
        self.filter_employees_by_status(self.status_filter.currentText())

    def show_add_employee_dialog(self):
        dialog = AddEmployeeDialog(self)
        if dialog.exec() == QDialog.Accepted:
            employee_data = dialog.get_employee_data()
            self.add_employee(employee_data)

    def add_employee(self, data):
        new_employee = [
            str(self.next_id),
            data['lastname'],
            data['firstname'],
            data['patronymic'],
            data['phone'],
            data['email'],
            data['position'],
            data['branch'],
            "Работает"
        ]
        self.all_employees_data.append(new_employee)
        self.next_id += 1
        self.filter_employees_by_status(self.status_filter.currentText())
        QMessageBox.information(self, "Успешно", f"Сотрудник {data['lastname']} {data['firstname']} добавлен!")

    def on_employee_double_clicked(self, row, column):
        employee_id = self.table.item(row, 0).text()
        employee_lastname = self.table.item(row, 1).text()
        employee_firstname = self.table.item(row, 2).text()
        employee_patronymic = self.table.item(row, 3).text()
        employee_phone = self.table.item(row, 4).text()
        employee_email = self.table.item(row, 5).text()
        employee_position = self.table.item(row, 6).text()
        employee_branch = self.table.item(row, 7).text()
        employee_status = self.table.item(row, 8).text()

        employee_data = [
            employee_id, employee_lastname, employee_firstname, employee_patronymic,
            employee_phone, employee_email, employee_position, employee_branch, employee_status
        ]
        dialog = EmployeeDetailDialog(employee_data, self)

        dialog.employee_deleted.connect(self.delete_employee)

        if dialog.exec() == QDialog.Accepted:
            updated_data = dialog.get_updated_data()
            self.update_employee_data(employee_id, updated_data)

    def delete_employee(self, employee_id):
        for i, emp in enumerate(self.all_employees_data):
            if int(emp[0]) == employee_id:
                del self.all_employees_data[i]
                break

        self.filter_employees_by_status(self.status_filter.currentText())

        QMessageBox.information(self, "Успешно", f"Сотрудник удален из системы")

    def update_employee_data(self, employee_id, updated_data):

        for i, emp in enumerate(self.all_employees_data):
            if emp[0] == employee_id:
                self.all_employees_data[i][1] = updated_data['lastname']
                self.all_employees_data[i][2] = updated_data['firstname']
                self.all_employees_data[i][3] = updated_data['patronymic']
                self.all_employees_data[i][4] = updated_data['phone']
                self.all_employees_data[i][5] = updated_data['email']
                self.all_employees_data[i][6] = updated_data['position']
                self.all_employees_data[i][7] = updated_data['branch']
                self.all_employees_data[i][8] = updated_data['status']
                break

        self.filter_employees_by_status(self.status_filter.currentText())
        QMessageBox.information(self, "Успешно", "Данные сотрудника обновлены")


class UserDetailDialog(QDialog):
    status_changed = Signal(str)

    def __init__(self, user_data, parent=None):
        super().__init__(parent)
        self.user_data = user_data
        self.setWindowTitle(f"Пользователь: {user_data[0]}")
        self.setMinimumSize(500, 400)
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

        #Заголовок с именем пользователя
        title_label = QLabel(f"Пользователь: {self.user_data[0]}")
        title_label.setProperty("heading", True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title_label)

        #Информация о пользователе
        info_group = QGroupBox("Информация о пользователе")
        info_layout = QGridLayout(info_group)
        info_layout.setVerticalSpacing(10)
        info_layout.setHorizontalSpacing(20)

        info_layout.addWidget(QLabel("Email:"), 0, 0)
        info_layout.addWidget(QLabel(self.user_data[1]), 0, 1)

        info_layout.addWidget(QLabel("Дата регистрации:"), 1, 0)
        info_layout.addWidget(QLabel("15.03.2026"), 1, 1)

        info_layout.addWidget(QLabel("Кол-во заказов:"), 2, 0)
        info_layout.addWidget(QLabel("25"), 2, 1)

        info_layout.addWidget(QLabel("Статус:"), 3, 0)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Активен", "Заблокирован"])
        self.status_combo.setCurrentText(self.user_data[2])
        info_layout.addWidget(self.status_combo, 3, 1)

        layout.addWidget(info_group)

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

    def get_updated_status(self):
        return self.status_combo.currentText()


class UsersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.all_users_data = [
            ["Козлов Сергей", "john@example.com", "Активен"],
            ["Джейн Смит", "jane@example.com", "Активен"],
            ["Боб Уилсон", "bob@example.com", "Заблокирован"],
            ["Алиса Браун", "alice@example.com", "Активен"],
            ["Чарли Дэвис", "charlie@example.com", "Активен"],
            ["Ива Миллер", "eve@example.com", "Активен"],
        ]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Все пользователи")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title)

        #Панель поиска
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск пользователей по имени пользователя или почте...")
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
        search_btn.clicked.connect(self.search_users)

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

        #Таблица пользователей
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Имя пользователя", "Email", "Статус"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
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

        self.populate_users()
        self.table.cellDoubleClicked.connect(self.on_user_double_clicked)

        layout.addWidget(self.table)

    def populate_users(self, data=None):
        if data is None:
            data = self.all_users_data

        self.table.setRowCount(len(data))

        for row, user_data in enumerate(data):
            for col, value in enumerate(user_data):
                item = QTableWidgetItem(str(value))

                if col == 0 or col == 2:
                    item.setTextAlignment(Qt.AlignCenter)

                if col == 2:
                    if value == "Активен":
                        item.setForeground(QColor("#28a745"))
                        item.setBackground(QColor("#e8f5e9"))
                    else:
                        item.setForeground(QColor("#dc3545"))
                        item.setBackground(QColor("#f8d7da"))

                self.table.setItem(row, col, item)

    def search_users(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.filter_users(self.filter_combo.currentText())
            return

        filtered_data = []
        for user in self.all_users_data:
            if (search_text in user[0].lower() or  # Поиск по имени
                    search_text in user[1].lower()):  # Поиск по email
                filtered_data.append(user)

        if filtered_data:
            current_filter = self.filter_combo.currentText()
            if current_filter != "Все пользователи":
                status_map = {
                    "Активные": "Активен",
                    "Заблокированные": "Заблокирован",
                }
                filter_status = status_map.get(current_filter)
                if filter_status:
                    filtered_data = [u for u in filtered_data if u[2] == filter_status]
            self.populate_users(filtered_data)
        else:
            QMessageBox.information(self, "Поиск", "Ничего не найдено")
            self.filter_users(self.filter_combo.currentText())

    def clear_search(self):
        self.search_input.clear()
        self.filter_users(self.filter_combo.currentText())

    def filter_users(self, filter_text):
        if filter_text == "Все пользователи":
            self.populate_users(self.all_users_data)
        elif filter_text == "Активные":
            filtered = [u for u in self.all_users_data if u[2] == "Активен"]
            self.populate_users(filtered)
        elif filter_text == "Заблокированные":
            filtered = [u for u in self.all_users_data if u[2] == "Заблокирован"]
            self.populate_users(filtered)
        elif filter_text == "Новые":
            filtered = self.all_users_data[:2]
            for u in filtered:
                u[2] = "Активен"
            self.populate_users(filtered)

    def on_user_double_clicked(self, row, column):
        user_name = self.table.item(row, 0).text()
        user_email = self.table.item(row, 1).text()
        user_status = self.table.item(row, 2).text()

        user_data = [user_name, user_email, user_status]
        dialog = UserDetailDialog(user_data, self)

        if dialog.exec() == QDialog.Accepted:
            new_status = dialog.get_updated_status()
            self.update_user_status(row, new_status)

    def update_user_status(self, row, new_status):
        user_name = self.table.item(row, 0).text()
        for i, user in enumerate(self.all_users_data):
            if user[0] == user_name:
                self.all_users_data[i][2] = new_status
                break

        self.filter_users(self.filter_combo.currentText())



class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()

        #Данные для отчетов
        self.sales_data = [
            {
                'article': 'СБ-001',
                'name': 'Синнабон Классический',
                'total_sales': 145,
                'cost': 174000,
                'revenue': 217500,
                'revenue_percent': 18.2,
                'profit': 43500,
                'profit_percent': 25.0
            },
            {
                'article': 'СБ-002',
                'name': 'Синнабон Шоколадный',
                'total_sales': 132,
                'cost': 158400,
                'revenue': 198000,
                'revenue_percent': 16.6,
                'profit': 39600,
                'profit_percent': 25.0
            },
            {
                'article': 'КБ-001',
                'name': 'Кремобон Ванильный',
                'total_sales': 98,
                'cost': 117600,
                'revenue': 147000,
                'revenue_percent': 12.3,
                'profit': 29400,
                'profit_percent': 25.0
            },
            {
                'article': 'ПЖ-001',
                'name': 'Пирожное Корзиночка',
                'total_sales': 155,
                'cost': 155000,
                'revenue': 193750,
                'revenue_percent': 16.2,
                'profit': 38750,
                'profit_percent': 25.0
            },
            {
                'article': 'ТР-001',
                'name': 'Торт Наполеон',
                'total_sales': 63,
                'cost': 126000,
                'revenue': 157500,
                'revenue_percent': 13.2,
                'profit': 31500,
                'profit_percent': 25.0
            },
            {
                'article': 'НП-001',
                'name': 'Капучино',
                'total_sales': 258,
                'cost': 77400,
                'revenue': 129000,
                'revenue_percent': 10.8,
                'profit': 51600,
                'profit_percent': 66.7
            },
        ]

        #Данные по заведениям
        self.branches_data = [
            {
                'branch': 'ТЦ "МЕГА"',
                'total_sales': 452,
                'revenue': 678000,
                'revenue_percent': 28.5,
                'profit': 169500,
                'profit_percent': 25.0,
                'avg_check': 1500
            },
            {
                'branch': 'ТЦ "ГУМ"',
                'total_sales': 389,
                'revenue': 583500,
                'revenue_percent': 24.5,
                'profit': 145875,
                'profit_percent': 25.0,
                'avg_check': 1500
            },
            {
                'branch': 'ТЦ "АВИАПАРК"',
                'total_sales': 412,
                'revenue': 618000,
                'revenue_percent': 26.0,
                'profit': 154500,
                'profit_percent': 25.0,
                'avg_check': 1500
            },
            {
                'branch': 'ТЦ "ЕВРОПЕЙСКИЙ"',
                'total_sales': 298,
                'revenue': 447000,
                'revenue_percent': 18.8,
                'profit': 111750,
                'profit_percent': 25.0,
                'avg_check': 1500
            },
            {
                'branch': 'ТЦ "РИО"',
                'total_sales': 256,
                'revenue': 384000,
                'revenue_percent': 16.1,
                'profit': 96000,
                'profit_percent': 25.0,
                'avg_check': 1500
            },
        ]

        #Текущий активный отчет
        self.current_report = "sales"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        #Панель статусов
        self.create_status_bar(layout)

        #Заголовок
        self.title_label = QLabel("Общий отчёт по продажам")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(self.title_label)

        #Панель выбора периода
        report_selection1 = QHBoxLayout()

        self.report_type = QComboBox()
        self.report_type.addItems([
            "День",
            "Неделя",
            "Месяц",
            "Квартал",
            "Год"
        ])
        self.report_type.setFixedWidth(200)
        self.report_type.setFixedHeight(35)
        self.report_type.currentTextChanged.connect(self.on_period_changed)

        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        self.date_from.setFixedWidth(120)
        self.date_from.setFixedHeight(35)

        #Панель выбора группировки
        self.report_group = QComboBox()
        self.report_group.addItems([
            "По филиалам",
            "По категориям"
        ])
        self.report_group.setFixedWidth(200)
        self.report_group.setFixedHeight(35)
        self.report_group.currentTextChanged.connect(self.on_grouping_changed)

        #Панель выбора сортировки
        self.report_sort = QComboBox()
        self.report_sort.addItems([
            "По возрастанию",
            "По убыванию"
        ])
        self.report_sort.setFixedWidth(200)
        self.report_sort.setFixedHeight(35)

        #Панель формирования отчёта
        self.generate_btn = QPushButton("Сформировать отчет")
        self.generate_btn.setFixedHeight(35)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 0 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_report)

        #Панель сохранения отчёта
        self.export_btn = QPushButton("Сохранить отчет")
        self.export_btn.setFixedHeight(35)
        self.export_btn.setStyleSheet("""
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
        self.export_btn.clicked.connect(self.export_report)

        #Добавляем элементы в layout
        report_selection1.addWidget(QLabel("Период:"))
        report_selection1.addWidget(self.report_type)
        report_selection1.addWidget(QLabel("с"))
        report_selection1.addWidget(self.date_from)
        report_selection1.addStretch()
        layout.addLayout(report_selection1)

        report_selection2 = QHBoxLayout()
        report_selection2.addWidget(QLabel("Группировать:"))
        report_selection2.addWidget(self.report_group)
        report_selection2.addStretch()
        layout.addLayout(report_selection2)

        report_selection3 = QHBoxLayout()
        report_selection3.addWidget(QLabel("Сортировать:"))
        report_selection3.addWidget(self.report_sort)
        report_selection3.addStretch()
        layout.addLayout(report_selection3)

        report_selection4 = QHBoxLayout()
        report_selection4.addWidget(self.generate_btn)
        report_selection4.addWidget(self.export_btn)
        report_selection4.addStretch()
        layout.addLayout(report_selection4)

        #Таблица
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                selection-background-color: #e6f2fa;
                font-size: 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
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
                font-size: 12px;
            }
        """)

        layout.addWidget(self.table)

        #Инициализация таблицы
        self.setup_sales_table()

    def create_status_bar(self, layout):
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)

        self.status_buttons = {}
        statuses = [
            ("Отчёт по продажам", "sales"),
            ("Отчёт по заведениям", "branches"),
            ("Отчёт по изделиям", "categories")
        ]

        for status_text, status_key in statuses:
            btn = QPushButton(status_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFlat(True)
            btn.status_key = status_key

            if status_key == "sales":
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

            btn.clicked.connect(lambda checked, s=status_key: self.on_status_filter_clicked(s))
            self.status_buttons[status_key] = btn
            status_layout.addWidget(btn)

        status_layout.addStretch()
        layout.addLayout(status_layout)

    def setup_sales_table(self):
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Артикул",
            "Наименование",
            "Кол-во продаж",
            "Себестоимость",
            "Выручка",
            "Выручка %",
            "Прибыль",
            "Прибыль %"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.populate_sales_table()

    def setup_branches_table(self):
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Наименование",
            "Общее кол-во заказов",
            "Кол-во  завершённых заказов",
            "Кол-во отменённых заказов",
            "Выручка",
            "Выручка %",
            "Прибыль",
            "Прибыль %",
            "Средний чек"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.populate_branches_table()

    def setup_categories_table(self):
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Артикул",
            "Общее кол-во продаж",
            "Выручка",
            "Выручка %",
            "Прибыль",
            "Прибыль %",
            "Наценка %"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.populate_categories_table()

    def populate_sales_table(self, data=None):
        if data is None:
            data = self.sales_data

        #Сортировка данных
        sort_order = self.report_sort.currentText()
        data = self.sort_data(data, sort_order)

        self.table.setRowCount(len(data))

        total_revenue = sum(item['revenue'] for item in data)

        for row, item in enumerate(data):
            #Артикул
            self.table.setItem(row, 0, QTableWidgetItem(item['article']))

            #Наименование
            self.table.setItem(row, 1, QTableWidgetItem(item['name']))

            #Кол-во продаж
            sales_item = QTableWidgetItem(str(item['total_sales']))
            sales_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 2, sales_item)

            #Себестоимость
            cost_item = QTableWidgetItem(f"{item['cost']:,.0f}".replace(',', ' '))
            cost_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 3, cost_item)

            #Выручка
            revenue_item = QTableWidgetItem(f"{item['revenue']:,.0f}".replace(',', ' '))
            revenue_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 4, revenue_item)

            #Выручка %
            revenue_percent = (item['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            percent_item = QTableWidgetItem(f"{revenue_percent:.1f}%")
            percent_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 5, percent_item)

            #Прибыль
            profit_item = QTableWidgetItem(f"{item['profit']:,.0f}".replace(',', ' '))
            profit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if item['profit'] > 0:
                profit_item.setForeground(QColor(40, 167, 69))
            self.table.setItem(row, 6, profit_item)

            #Прибыль %
            profit_percent_item = QTableWidgetItem(f"{item['profit_percent']:.1f}%")
            profit_percent_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if item['profit_percent'] > 25:
                profit_percent_item.setForeground(QColor(40, 167, 69))
            elif item['profit_percent'] < 15:
                profit_percent_item.setForeground(QColor(220, 53, 69))
            self.table.setItem(row, 7, profit_percent_item)

        self.add_sales_total_row(data)

    def populate_branches_table(self, data=None):
        if data is None:
            data = self.branches_data

        #Сортировка данных
        sort_order = self.report_sort.currentText()
        data = self.sort_data(data, sort_order, 'revenue')

        self.table.setRowCount(len(data))

        total_revenue = sum(item['revenue'] for item in data)

        for row, item in enumerate(data):
            #Заведение
            self.table.setItem(row, 0, QTableWidgetItem(item['branch']))

            #Кол-во продаж
            sales_item = QTableWidgetItem(str(item['total_sales']))
            sales_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 1, sales_item)

            #Выручка
            revenue_item = QTableWidgetItem(f"{item['revenue']:,.0f}".replace(',', ' '))
            revenue_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 2, revenue_item)

            #Выручка %
            revenue_percent = (item['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            percent_item = QTableWidgetItem(f"{revenue_percent:.1f}%")
            percent_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 3, percent_item)

            #Прибыль
            profit_item = QTableWidgetItem(f"{item['profit']:,.0f}".replace(',', ' '))
            profit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if item['profit'] > 0:
                profit_item.setForeground(QColor(40, 167, 69))
            self.table.setItem(row, 4, profit_item)

            #Прибыль %
            profit_percent_item = QTableWidgetItem(f"{item['profit_percent']:.1f}%")
            profit_percent_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 5, profit_percent_item)

            #Средний чек
            avg_check_item = QTableWidgetItem(f"{item['avg_check']:,.0f}".replace(',', ' '))
            avg_check_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 6, avg_check_item)

        self.add_branches_total_row(data)

    def populate_categories_table(self, data=None):
        if data is None:
            data = self.categories_data

        #Сортировка данных
        sort_order = self.report_sort.currentText()
        data = self.sort_data(data, sort_order, 'revenue')

        self.table.setRowCount(len(data))

        total_revenue = sum(item['revenue'] for item in data)

        for row, item in enumerate(data):
            #Категория
            self.table.setItem(row, 0, QTableWidgetItem(item['category']))

            #Кол-во продаж
            sales_item = QTableWidgetItem(str(item['total_sales']))
            sales_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 1, sales_item)

            #Выручка
            revenue_item = QTableWidgetItem(f"{item['revenue']:,.0f}".replace(',', ' '))
            revenue_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 2, revenue_item)

            #Выручка %
            revenue_percent = (item['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            percent_item = QTableWidgetItem(f"{revenue_percent:.1f}%")
            percent_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 3, percent_item)

            #Прибыль
            profit_item = QTableWidgetItem(f"{item['profit']:,.0f}".replace(',', ' '))
            profit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            if item['profit'] > 0:
                profit_item.setForeground(QColor(40, 167, 69))
            self.table.setItem(row, 4, profit_item)

            #Прибыль %
            profit_percent_item = QTableWidgetItem(f"{item['profit_percent']:.1f}%")
            profit_percent_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 5, profit_percent_item)

            #Популярный товар
            self.table.setItem(row, 6, QTableWidgetItem(item['popular_product']))

        self.add_categories_total_row(data)

    def add_sales_total_row(self, data):
        total_sales = sum(item['total_sales'] for item in data)
        total_cost = sum(item['cost'] for item in data)
        total_revenue = sum(item['revenue'] for item in data)
        total_profit = total_revenue - total_cost
        avg_profit_percent = (total_profit / total_cost * 100) if total_cost > 0 else 0

        self.table.setRowCount(self.table.rowCount() + 1)
        row = self.table.rowCount() - 1
        font = self.table.font()
        font.setBold(True)

        items = [
            ("ИТОГО:", 0), ("", 1),
            (f"{total_sales}", 2),
            (f"{total_cost:,.0f}".replace(',', ' '), 3),
            (f"{total_revenue:,.0f}".replace(',', ' '), 4),
            ("100%", 5),
            (f"{total_profit:,.0f}".replace(',', ' '), 6),
            (f"{avg_profit_percent:.1f}%", 7)
        ]

        for text, col in items:
            if text:
                item = QTableWidgetItem(text)
                item.setFont(font)
                item.setBackground(QColor(248, 249, 250))
                if col in [6, 7] and total_profit > 0:
                    item.setForeground(QColor(40, 167, 69))
                self.table.setItem(row, col, item)

    def add_branches_total_row(self, data):
        total_sales = sum(item['total_sales'] for item in data)
        total_revenue = sum(item['revenue'] for item in data)
        total_profit = sum(item['profit'] for item in data)
        avg_check = total_revenue / total_sales if total_sales > 0 else 0

        self.table.setRowCount(self.table.rowCount() + 1)
        row = self.table.rowCount() - 1
        font = self.table.font()
        font.setBold(True)

        items = [
            ("ИТОГО:", 0),
            (f"{total_sales}", 1),
            (f"{total_revenue:,.0f}".replace(',', ' '), 2),
            ("100%", 3),
            (f"{total_profit:,.0f}".replace(',', ' '), 4),
            (f"{(total_profit / total_revenue * 100):.1f}%" if total_revenue > 0 else "0%", 5),
            (f"{avg_check:,.0f}".replace(',', ' '), 6)
        ]

        for text, col in items:
            item = QTableWidgetItem(text)
            item.setFont(font)
            item.setBackground(QColor(248, 249, 250))
            if col in [4, 5] and total_profit > 0:
                item.setForeground(QColor(40, 167, 69))
            self.table.setItem(row, col, item)

    def add_categories_total_row(self, data):
        total_sales = sum(item['total_sales'] for item in data)
        total_revenue = sum(item['revenue'] for item in data)
        total_profit = sum(item['profit'] for item in data)

        self.table.setRowCount(self.table.rowCount() + 1)
        row = self.table.rowCount() - 1
        font = self.table.font()
        font.setBold(True)

        items = [
            ("ИТОГО:", 0),
            (f"{total_sales}", 1),
            (f"{total_revenue:,.0f}".replace(',', ' '), 2),
            ("100%", 3),
            (f"{total_profit:,.0f}".replace(',', ' '), 4),
            (f"{(total_profit / total_revenue * 100):.1f}%" if total_revenue > 0 else "0%", 5),
            ("", 6)
        ]

        for text, col in items:
            if text:
                item = QTableWidgetItem(text)
                item.setFont(font)
                item.setBackground(QColor(248, 249, 250))
                if col in [4, 5] and total_profit > 0:
                    item.setForeground(QColor(40, 167, 69))
                self.table.setItem(row, col, item)

    def sort_data(self, data, sort_order, key='total_sales'):
        reverse = (sort_order == "По убыванию")
        return sorted(data, key=lambda x: x.get(key, 0), reverse=reverse)

    def generate_report(self):
        date_from = self.date_from.date().toString("dd.MM.yyyy")
        date_to = self.date_to.date().toString("dd.MM.yyyy")

        print(f"Генерация отчета:")
        print(f"  Тип: {self.current_report}")
        print(f"  Период: {date_from} - {date_to}")
        print(f"  Группировка: {self.report_group.currentText()}")
        print(f"  Сортировка: {self.report_sort.currentText()}")

        #Обновляем таблицу в зависимости от текущего отчета
        if self.current_report == "sales":
            self.populate_sales_table()
        elif self.current_report == "branches":
            self.populate_branches_table()
        elif self.current_report == "categories":
            self.populate_categories_table()

        QMessageBox.information(
            self,
            "Отчет сформирован",
            f"Отчет '{self.get_report_title()}' успешно сформирован за период {date_from} - {date_to}"
        )

    def export_report(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить отчет",
            f"{self.get_report_filename()}_{QDate.currentDate().toString('dd_MM_yyyy')}.csv",
            "CSV файлы (*.csv);;Excel файлы (*.xlsx);;Все файлы (*.*)"
        )

        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)

                    # Записываем заголовки
                    headers = [
                        self.table.horizontalHeaderItem(i).text()
                        for i in range(self.table.columnCount())
                    ]
                    writer.writerow(headers)

                    #Записываем данные
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)

                QMessageBox.information(
                    self,
                    "Экспорт завершен",
                    f"Отчет успешно сохранен в файл:\n{file_path}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Ошибка экспорта",
                    f"Не удалось сохранить отчет:\n{str(e)}"
                )

    def on_status_filter_clicked(self, status_key):
        self.current_report = status_key

        #Обновляем стили всех кнопок
        for btn_status, btn in self.status_buttons.items():
            if btn_status == status_key:
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

        #Загружаем соответствующий отчет
        if status_key == "sales":
            self.title_label.setText("Общий отчёт по продажам")
            self.setup_sales_table()
        elif status_key == "branches":
            self.title_label.setText("Отчёт по заведениям")
            self.setup_branches_table()
        elif status_key == "categories":
            self.title_label.setText("Отчёт по изделиям")
            self.setup_categories_table()

    def on_period_changed(self, period):
        today = QDate.currentDate()

        if period == "День":
            self.date_from.setDate(today)
            self.date_to.setDate(today)
        elif period == "Неделя":
            self.date_from.setDate(today.addDays(-7))
            self.date_to.setDate(today)
        elif period == "Месяц":
            self.date_from.setDate(today.addMonths(-1))
            self.date_to.setDate(today)
        elif period == "Квартал":
            self.date_from.setDate(today.addMonths(-3))
            self.date_to.setDate(today)
        elif period == "Год":
            self.date_from.setDate(today.addYears(-1))
            self.date_to.setDate(today)

    def on_grouping_changed(self, grouping):
        if grouping == "По заведениям" and self.current_report != "branches":
            self.on_status_filter_clicked("branches")
        elif grouping == "По категориям" and self.current_report != "categories":
            self.on_status_filter_clicked("categories")

    def get_report_title(self):
        titles = {
            "sales": "Отчет по продажам",
            "branches": "Отчет по заведениям",
            "categories": "Отчет по изделиям"
        }
        return titles.get(self.current_report, "Отчет")

    def get_report_filename(self):
        names = {
            "sales": "report_sales",
            "branches": "report_branches",
            "categories": "report_categories"
        }
        return names.get(self.current_report, "report")


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
        layout.setSpacing(15)

        #Заголовок
        title = QLabel("Добавление филиала")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
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
        form_layout.addWidget(self.phone_input, 2, 1)

        #Статус
        form_layout.addWidget(QLabel("Статус:"), 4, 0)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Открыт", "Закрыт"])
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

        self.accept()

    def get_bakery_data(self):
        return {
            'name': self.name_input.text().strip(),
            'address': self.address_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'status': self.status_combo.currentText(),
        }


class BakeryDetailDialog(QDialog):
    status_changed = Signal(str)

    def __init__(self, bakery_data, parent=None):
        super().__init__(parent)
        self.bakery_data = bakery_data
        self.setWindowTitle(f"Филиал: {bakery_data[0]}")
        self.setMinimumSize(500, 400)
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

        #Заголовок с названием филиала
        title_label = QLabel(f"Филиал: {self.bakery_data[0]}")
        title_label.setProperty("heading", True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title_label)

        #Информация о филиале
        info_group = QGroupBox("Информация о филиале")
        info_layout = QGridLayout(info_group)
        info_layout.setVerticalSpacing(10)
        info_layout.setHorizontalSpacing(20)

        info_layout.addWidget(QLabel("Адрес:"), 0, 0)
        self.address_input = QLineEdit(self.bakery_data[1])
        self.address_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
            }
        """)
        info_layout.addWidget(self.address_input, 0, 1)

        info_layout.addWidget(QLabel("Телефон:"), 1, 0)
        self.phone_input = QLineEdit(self.bakery_data[2])
        self.phone_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 13px;
            }
        """)
        info_layout.addWidget(self.phone_input, 1, 1)

        info_layout.addWidget(QLabel("Статус:"), 2, 0)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Открыт", "Закрыт"])
        self.status_combo.setCurrentText(self.bakery_data[3])
        self.status_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 13px;
            }
        """)
        info_layout.addWidget(self.status_combo, 2, 1)

        layout.addWidget(info_group)

        #Кнопки Ок и Отмена
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
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

    def get_updated_data(self):
        return {
            'address': self.address_input.text(),
            'phone': self.phone_input.text(),
            'status': self.status_combo.currentText()
        }


class BakeriesPage(QWidget):
    def __init__(self):
        super().__init__()
        #Данные филиалов
        self.bakeries_data = [
            ["Дульсе", "С. Молочное Ул. Попова 17", "+7(999)111-22-33", "Открыт"],
            ["Звукоуловитель", "ул. Ленина, 24", "+7(999)222-33-44", "Открыт"],
            ["Октябрьский", "пр. Мира, 5", "+7(999)333-44-55", "Закрыт"],
            ["Нагорный", "ул. Советская, 12", "+7(999)444-55-66", "Открыт"],
            ["Европейский", "ул. Гагарина, 8", "+7(999)555-66-77", "Открыт"],
            ["Волкова", "ул. Пушкина, 3", "+7(999)666-77-88", "Открыт"],
        ]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        #Заголовок
        title = QLabel("Все филиалы")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title)

        #Поиск и кнопки
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

        self.add_btn = QPushButton("+ Добавить филиал")
        self.add_btn.setFixedHeight(35)
        self.add_btn.setStyleSheet("""
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
        self.add_btn.clicked.connect(self.show_add_bakery_dialog)

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
        search_layout.addWidget(self.add_btn)

        layout.addLayout(search_layout)

        #Таблица филиалов
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Наименование", "Адрес", "Телефон", "Статус"
        ])

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

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

        self.table.cellDoubleClicked.connect(self.on_bakery_double_clicked)

        #Заполнение данными
        self.populate_bakeries()

        layout.addWidget(self.table)

    def populate_bakeries(self, data=None):
        if data is None:
            data = self.bakeries_data

        self.table.setRowCount(len(data))

        for row, bakery_data in enumerate(data):
            for col, value in enumerate(bakery_data):
                item = QTableWidgetItem(str(value))

                if col == 3:
                    item.setTextAlignment(Qt.AlignCenter)
                    if value == "Открыт":
                        item.setForeground(QColor("#28a745"))
                    else:
                        item.setForeground(QColor("#dc3545"))

                self.table.setItem(row, col, item)

    def show_add_bakery_dialog(self):
        dialog = AddBakeryDialog(self)
        if dialog.exec() == QDialog.Accepted:
            bakery_data = dialog.get_bakery_data()
            self.add_bakery(bakery_data)

    def add_bakery(self, data):
        new_bakery = [
            data['name'],
            data['address'],
            data['phone'],
            data['status']
        ]
        self.bakeries_data.append(new_bakery)
        self.populate_bakeries()

    def search_bakeries(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.populate_bakeries()
            return

        filtered_data = []
        for bakery in self.bakeries_data:
            if (search_text in bakery[0].lower() or  #Поиск по названию
                    search_text in bakery[1].lower() or  #Поиск по адресу
                    search_text in bakery[2].lower()):  #Поиск по телефону
                filtered_data.append(bakery)

        if filtered_data:
            self.populate_bakeries(filtered_data)
        else:
            QMessageBox.information(self, "Поиск", "Ничего не найдено")
            self.populate_bakeries()

    def clear_search(self):
        self.search_input.clear()
        self.populate_bakeries()

    def on_bakery_double_clicked(self, row, column):
        bakery_name = self.table.item(row, 0).text()
        bakery_address = self.table.item(row, 1).text()
        bakery_phone = self.table.item(row, 2).text()
        bakery_status = self.table.item(row, 3).text()

        bakery_data = [bakery_name, bakery_address, bakery_phone, bakery_status]
        dialog = BakeryDetailDialog(bakery_data, self)

        if dialog.exec() == QDialog.Accepted:
            updated_data = dialog.get_updated_data()
            self.update_bakery_data(row, updated_data)

    def update_bakery_data(self, row, updated_data):
        bakery_name = self.table.item(row, 0).text()
        for i, bakery in enumerate(self.bakeries_data):
            if bakery[0] == bakery_name:
                self.bakeries_data[i][1] = updated_data['address']
                self.bakeries_data[i][2] = updated_data['phone']
                self.bakeries_data[i][3] = updated_data['status']
                break

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
        self.users_page = UsersPage()
        self.reports_page = ReportsPage()
        self.bakeries_page = BakeriesPage()

        #Добавление страниц в стек
        self.stacked_widget.addWidget(self.orders_page)
        self.stacked_widget.addWidget(self.catalog_page)
        self.stacked_widget.addWidget(self.employees_page)
        self.stacked_widget.addWidget(self.users_page)
        self.stacked_widget.addWidget(self.reports_page)
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
        sections = ["Заказы", "Каталог", "Сотрудники", "Пользователи", "Отчёты", "Филиалы"]

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
        elif page_name == "Пользователи":
            self.stacked_widget.setCurrentWidget(self.users_page)
        elif page_name == "Отчёты":
            self.stacked_widget.setCurrentWidget(self.reports_page)
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


class ApplicationController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')

        self.login_window = LoginScreen()
        self.login_window.login_successful.connect(self.show_main_window)

        self.main_window = None

    def show_main_window(self):
        self.main_window = MainApplication()
        self.main_window.show()

    def run(self):
        self.login_window.show()
        return self.app.exec()


def main():
    controller = ApplicationController()
    sys.exit(controller.run())


if __name__ == "__main__":
    main()