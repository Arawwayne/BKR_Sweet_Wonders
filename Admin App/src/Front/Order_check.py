import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QFrame, QDialog, QGridLayout, QComboBox, QMessageBox,
    QDialogButtonBox, QGroupBox
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QFont, QColor, QIcon


class OrderDetailDialog(QDialog):

    #Сигнал для обновления статуса заказа
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

        title_label = QLabel(f"Заказ: {self.order_data['order_number']}")
        title_label.setProperty("heading", True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #0078d7; margin-bottom: 10px;")
        layout.addWidget(title_label)

        info_group = QGroupBox("Информация о заказе")
        info_layout = QGridLayout(info_group)
        info_layout.setVerticalSpacing(10)
        info_layout.setHorizontalSpacing(20)

        #Данные пользователя и заведения
        row = 0
        info_layout.addWidget(QLabel("Наименование пользователя:"), row, 0)
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
            #Название изделия
            self.items_table.setItem(row, 0, QTableWidgetItem(item['name']))

            #Количество
            quantity_item = QTableWidgetItem(str(item['quantity']))
            quantity_item.setTextAlignment(Qt.AlignCenter)
            self.items_table.setItem(row, 1, quantity_item)

            #Итого
            total_item = QTableWidgetItem(f"{item['total']:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.items_table.setItem(row, 2, total_item)

    def get_updated_status(self):
        return self.status_combo.currentText()


class OrdersScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление заказами")
        self.setMinimumSize(1200, 600)

        self.orders_data = {
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
                'items': [
                    {'name': 'Синнабон корейский', 'quantity': 1, 'total': 89.00}
                ]
            },
            "00002": {
                'order_number': '00002',
                'username': 'Мария Перменова Львовна',
                'phone': '+79229281777',
                'created_date': '09.09.2026',
                'completed_date': '17:30 10.09.2026',
                'establishment': 'Мягкая булка 17',
                'address': 'С. Молочное Ул. Попова 17',
                'total': '1000.00',
                'status': 'В работе',
                'items': [
                    {'name': 'Синнабон корейский', 'quantity': 2, 'total': 240.00},
                    {'name': 'Кремобон карамельный', 'quantity': 1, 'total': 160.00},
                    {'name': 'Дополнительные изделия', 'quantity': 3, 'total': 600.00}
                ]
            }
        }

        #Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        #Верхняя навигационная панель
        self.create_top_navbar(main_layout)

        #Панель статусов заказов
        self.create_status_bar(main_layout)

        #Панель поиска
        self.create_search_bar(main_layout)

        #Таблица заказов
        self.create_orders_table(main_layout)

        #Заполняем тестовыми данными
        self.populate_table()

        self.table.cellDoubleClicked.connect(self.on_order_double_clicked)

    def create_top_navbar(self, layout):
        navbar = QHBoxLayout()
        navbar.setSpacing(20)

        sections = ["Заказы", "Каталог", "Сотрудники", "Пользователи", "Отчёты", "Филиалы"]
        for section in sections:
            btn = QPushButton(section)
            btn.setFlat(True)
            btn.setCursor(Qt.PointingHandCursor)
            font = QFont()
            font.setPointSize(11)
            if section == "Заказы":
                font.setBold(True)
                btn.setStyleSheet("color: #0078d7;")
            btn.setFont(font)
            navbar.addWidget(btn)

        navbar.addStretch()

        user_label = QLabel("userLastname")
        font = QFont()
        font.setPointSize(11)
        user_label.setFont(font)
        user_label.setStyleSheet("padding: 5px 10px; background-color: #f0f0f0; border-radius: 3px;")
        navbar.addWidget(user_label)

        layout.addLayout(navbar)

    def add_separator(self, layout):
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #e0e0e0; max-height: 1px;")
        layout.addWidget(separator)

    def create_status_bar(self, layout):
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)

        statuses = ["Все заказы", "Открытые", "В работе", "Готовые", "Завершённые", "Отменённые"]

        for status in statuses:
            btn = QPushButton(status)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFlat(True)

            font = QFont()
            font.setPointSize(10)
            btn.setFont(font)

            if status == "Все заказы":
                btn.setStyleSheet("""
                    QPushButton {
                        color: #0078d7;
                        border-bottom: 2px solid #0078d7;
                        padding: 5px 0px;
                    }
                    QPushButton:hover {
                        color: #005a9e;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        color: #666;
                        padding: 5px 0px;
                    }
                    QPushButton:hover {
                        color: #0078d7;
                    }
                """)

            status_layout.addWidget(btn)

        status_layout.addStretch()
        layout.addLayout(status_layout)

    def create_search_bar(self, layout):
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск:")
        self.search_input.setFixedHeight(35)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #0078d7;
            }
        """)

        search_btn = QPushButton("Найти")
        search_btn.setFixedSize(80, 35)
        search_btn.setCursor(Qt.PointingHandCursor)
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
        search_btn.clicked.connect(self.search_orders)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        search_layout.addStretch()

        layout.addLayout(search_layout)

    def create_orders_table(self, layout):
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "№", "Заказа", "Имя пользователя", "Сумма заказа",
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
            }
            QTableWidget::item {
                padding: 8px;
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

    def populate_table(self):
        table_data = [
            ["00002", "Мария Перменова Львовна", "1000Р", "+79229281777", "09.09.2026", "17:30 10.09.2026", "В работе"],
            ["00001", "Васян", "89Р", "+79823145521", "09.09.2026", "11:30 12.09.2026", "Открыт"]
        ]

        self.table.setRowCount(len(table_data))

        for row, order_data in enumerate(table_data):
            for col, value in enumerate(order_data):
                item = QTableWidgetItem(str(value))

                if col in [0, 3, 4, 5, 6]:
                    item.setTextAlignment(Qt.AlignCenter)

                if col == 6:
                    item.setTextAlignment(Qt.AlignCenter)
                    if value == "В работе":
                        item.setForeground(QColor("#ff8c00"))
                        item.setBackground(QColor("#fff3e0"))
                    elif value == "Открыт":
                        item.setForeground(QColor("#28a745"))
                        item.setBackground(QColor("#e8f5e9"))

                self.table.setItem(row, col, item)

        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 120)
        self.table.setColumnWidth(6, 150)
        self.table.setColumnWidth(7, 100)

    def on_order_double_clicked(self, row, column):
        order_number_item = self.table.item(row, 0)
        if order_number_item:
            order_number = order_number_item.text()

            #Получаем полные данные заказа
            if order_number in self.orders_data:
                order_details = self.orders_data[order_number]

                #Создаем и показываем диалог
                dialog = OrderDetailDialog(order_details, self)

                #Подключаем обработчик изменения статуса
                if dialog.exec() == QDialog.Accepted:
                    new_status = dialog.get_updated_status()
                    self.update_order_status(order_number, new_status)

    def update_order_status(self, order_number, new_status):
        # Обновляем в данных
        if order_number in self.orders_data:
            self.orders_data[order_number]['status'] = new_status

        #Обновляем в таблице
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.text() == order_number:
                status_item = self.table.item(row, 6)
                if status_item:
                    status_item.setText(new_status)

                    #Обновляем цвета
                    if new_status == "В работе":
                        status_item.setForeground(QColor("#ff8c00"))
                        status_item.setBackground(QColor("#fff3e0"))
                    elif new_status == "Открыт":
                        status_item.setForeground(QColor("#28a745"))
                        status_item.setBackground(QColor("#e8f5e9"))
                    elif new_status == "Готов":
                        status_item.setForeground(QColor("#0078d7"))
                        status_item.setBackground(QColor("#e6f2fa"))
                    elif new_status == "Завершён":
                        status_item.setForeground(QColor("#6c757d"))
                        status_item.setBackground(QColor("#f8f9fa"))
                    elif new_status == "Отменён":
                        status_item.setForeground(QColor("#dc3545"))
                        status_item.setBackground(QColor("#f8d7da"))

                QMessageBox.information(self, "Успешно", f"Статус заказа {order_number} изменен на '{new_status}'")
                break

    def search_orders(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            QMessageBox.information(self, "Поиск", "Введите текст для поиска")
            return

        for row in range(self.table.rowCount()):
            match_found = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break

            if match_found:
                self.table.selectRow(row)
                break


def main():
    app = QApplication(sys.argv)

    window = OrdersScreen()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()