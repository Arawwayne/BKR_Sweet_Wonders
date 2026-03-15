import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QFrame, QDialog, QGridLayout, QComboBox, QMessageBox,
    QDialogButtonBox, QGroupBox, QStackedWidget, QTabWidget, QListWidget,
    QListWidgetItem, QTextEdit, QDateEdit, QSpinBox, QDoubleSpinBox,
    QCheckBox, QRadioButton, QButtonGroup, QSplitter, QTreeWidget,
    QTreeWidgetItem, QProgressBar, QSlider, QDial
)
from PySide6.QtCore import Qt, QSize, Signal, QDate, QTimer
from PySide6.QtGui import QFont, QColor, QIcon, QPixmap, QPainter, QPen
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
import random
from datetime import datetime, timedelta


class OrdersScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление заказами")
        self.setMinimumSize(1200, 600)

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

    def create_top_navbar(self, layout):
        navbar = QHBoxLayout()
        navbar.setSpacing(20)

        #Названия разделов
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


        layout.addLayout(navbar)

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

        #Поле поиска
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

        #Кнопка поиска
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

        #Настройка таблицы
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        #Стили
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
        #Данные из изображения
        data = [
            ["00002", "Мария Перменова Львовна", "1000Р", "+79229281777", "09.09.2026", "17:30 10.09.2026", "В работе"],
            ["00001", "Васян", "89Р", "+79823145521", "09.09.2026", "11:30 12.09.2026", "Открыт"]
        ]

        self.table.setRowCount(len(data))

        for row, order_data in enumerate(data):
            for col, value in enumerate(order_data):
                item = QTableWidgetItem(str(value))

                if col in [0, 3, 4, 5, 6]:  #№, Сумма, Телефон, Дата создания, Дата выполнения
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

        #Настраиваем размер колонок
        self.table.setColumnWidth(0, 80)  # №
        self.table.setColumnWidth(2, 200)  # Имя пользователя
        self.table.setColumnWidth(3, 100)  # Сумма
        self.table.setColumnWidth(4, 150)  # Телефон
        self.table.setColumnWidth(5, 120)  # Дата создания
        self.table.setColumnWidth(6, 150)  # Дата выполнения
        self.table.setColumnWidth(7, 100)  # Статус

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