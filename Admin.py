from IMS import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DashboardPanel(QWidget):
    def __init__(self, conn, parent=None):
        super().__init__(parent)
        self.conn = conn
        self.setGeometry(10, 10, 1140, 500)
        self.setStyleSheet("background-color: rgb(70, 70, 70); border-radius: 10px;")

        self.main_layout = QVBoxLayout(self)

        # Title
        title = QLabel("Dashboard")
        title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(title)

        # ✅ Store widgets for refresh later
        self.summary_layout = QHBoxLayout()
        self.graph_layout = QHBoxLayout()

        self.main_layout.addLayout(self.summary_layout)
        self.main_layout.addLayout(self.graph_layout)

        # ✅ Add low stock header layout (label + refresh button)
        low_stock_header = QHBoxLayout()
        self.low_stock_label = QLabel("Low Stock Products")
        self.low_stock_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self.low_stock_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        low_stock_header.addWidget(self.low_stock_label)

        # ✅ Refresh button
        self.refresh_btn = QPushButton("⟳ Refresh")
        self.refresh_btn.setFixedWidth(100)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(50, 150, 200);
                color: white;
                border-radius: 8px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(60, 170, 220);
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_dashboard)
        low_stock_header.addWidget(self.refresh_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(low_stock_header)

        # ✅ Create low stock table
        self.low_stock_table = QTableWidget()
        self.low_stock_table.setColumnCount(4)
        self.low_stock_table.setHorizontalHeaderLabels(["Product Name", "Type", "Quantity", "Reorder Level"])
        self.low_stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.low_stock_table.verticalHeader().setVisible(False)
        self.low_stock_table.setStyleSheet("""
            QTableWidget {
                background-color: #f8f9fa;
                alternate-background-color: #e9ecef;
                gridline-color: #b0b0b0;
                border-radius: 10px;
                font-size: 13px;
                selection-background-color: rgb(70,130,250);
                selection-color: white;
            }
            QHeaderView::section {
                background-color: rgb(50,150,200);
                color: white;
                font-weight: bold;
                border: none;
                padding: 6px;
            }
            QHeaderView::section:first { border-top-left-radius: 10px; }
            QHeaderView::section:last { border-top-right-radius: 10px; }
            QTableCornerButton::section { background-color: rgb(50,150,200); border: none; }
            QScrollBar:vertical {
                background: #e2e2e2;
                width: 10px;
                margin: 2px 0 2px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(130,180,230), stop:1 rgb(90,150,210));
                border-radius: 20px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgb(150,200,250), stop:1 rgb(100,160,220));
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
        """)
        self.main_layout.addWidget(self.low_stock_table)

        self.refresh_dashboard()

    def refresh_dashboard(self):
        """Refresh all dashboard data"""
        for i in reversed(range(self.summary_layout.count())):
            widget = self.summary_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        for i in reversed(range(self.graph_layout.count())):
            widget = self.graph_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        data = self.fetch_dashboard_data()

        # Summary stats
        for label, value in [
            ("Total Categories", data["total_categories"]),
            ("Total Issued Items", data["total_stockout"]),
            ("Total Products", data["total_products"]),
        ]:
            box = QLabel(f"{label}\n{value}")
            box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.setStyleSheet("""
                QLabel {
                    background-color: rgb(80, 80, 80);
                    color: white;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 16px;
                }
            """)
            self.summary_layout.addWidget(box)

        # Graphs
        from matplotlib import pyplot as plt
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

        # Pie Chart – Category Distribution
        fig1, ax1 = plt.subplots(figsize=(3.8, 3.8))
        categories, counts = zip(*data["category_distribution"]) if data["category_distribution"] else ([], [])
        if categories:
            ax1.pie(counts, labels=categories, autopct='%1.1f%%', startangle=90)
            ax1.set_title("Category Distribution", fontsize=10)
        else:
            ax1.text(0.5, 0.5, "No Data", ha='center', va='center')
        self.graph_layout.addWidget(FigureCanvas(fig1))
        plt.close(fig1)

        # Bar Graph – Top 5 Products by Quantity
        fig2, ax2 = plt.subplots(figsize=(4.5, 2.2))
        fig2.tight_layout(pad=2.0)
        product_names, quantities = zip(*data["top_products"]) if data["top_products"] else ([], [])
        if product_names:
            bars = ax2.bar(product_names, quantities)
            ax2.set_title("Top 5 Products by Quantity", fontsize=10)
            ax2.set_xticks(range(len(product_names)))
            ax2.set_xticklabels(product_names, rotation=30, ha='right', fontsize=7)
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2, height + 0.5, str(int(height)),
                         ha='center', va='bottom', fontsize=7, color='white')
        else:
            ax2.text(0.5, 0.5, "No Data", ha='center', va='center')
        self.graph_layout.addWidget(FigureCanvas(fig2))
        plt.close(fig2)

        # Line Chart – Stock Movement Trend
        fig3, ax3 = plt.subplots(figsize=(4.5, 3.8))
        ax3.plot(data["stock_movement"]["labels"], data["stock_movement"]["stockin"], marker='o', label="Stock In")
        ax3.plot(data["stock_movement"]["labels"], data["stock_movement"]["stockout"], marker='o', label="Stock Out")
        ax3.set_title("Stock Movement Trend", fontsize=10)
        ax3.legend()
        self.graph_layout.addWidget(FigureCanvas(fig3))
        plt.close(fig3)

        # ✅ Update Low Stock Table
        low_stock_data = data["low_stock_products"]
        self.low_stock_table.setRowCount(len(low_stock_data))
        for row, (product_name, type_name, quantity, reorder_level) in enumerate(low_stock_data):
            self.low_stock_table.setItem(row, 0, QTableWidgetItem(product_name))
            self.low_stock_table.setItem(row, 1, QTableWidgetItem(type_name))

            qty_item = QTableWidgetItem(str(quantity))
            if quantity <= reorder_level:
                qty_item.setForeground(QColor("red"))
            elif quantity <= reorder_level + 5:
                qty_item.setForeground(QColor("orange"))
            self.low_stock_table.setItem(row, 2, qty_item)
            self.low_stock_table.setItem(row, 3, QTableWidgetItem(str(reorder_level)))

    def fetch_dashboard_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM category")
        total_categories = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]
        cursor.execute("SELECT IFNULL(SUM(Quantity), 0) FROM stockout")
        total_stockout = cursor.fetchone()[0]
        cursor.execute("""
            SELECT c.CategoryName, COUNT(p.ProductID)
            FROM category c
            JOIN type t ON c.CategoryID = t.CategoryID
            JOIN products p ON t.TypeID = p.TypeID
            GROUP BY c.CategoryName
        """)
        category_distribution = cursor.fetchall()
        cursor.execute("""
            SELECT ProductName, Quantity
            FROM products
            ORDER BY Quantity DESC LIMIT 5
        """)
        top_products = cursor.fetchall()
        cursor.execute("""
            SELECT p.ProductID,
                   IFNULL(SUM(si.Quantity), 0) AS StockIn,
                   IFNULL(SUM(so.Quantity), 0) AS StockOut
            FROM products p
            LEFT JOIN stockin si ON p.ProductID = si.ProductID
            LEFT JOIN stockout so ON p.ProductID = so.ProductID
            GROUP BY p.ProductID
            ORDER BY p.ProductID ASC
        """)
        rows = cursor.fetchall()
        labels = [str(r[0]) for r in rows]
        stockin = [r[1] for r in rows]
        stockout = [r[2] for r in rows]
        cursor.execute("""
            SELECT p.ProductName, t.TypeName, p.Quantity, p.ReorderLevel
            FROM products p
            JOIN type t ON p.TypeID = t.TypeID
            WHERE p.Quantity <= p.ReorderLevel + 5
            ORDER BY p.Quantity ASC
        """)
        low_stock_products = cursor.fetchall()
        cursor.close()
        return {
            "total_categories": total_categories,
            "total_products": total_products,
            "total_stockout": total_stockout,
            "category_distribution": category_distribution,
            "top_products": top_products,
            "stock_movement": {
                "labels": labels,
                "stockin": stockin,
                "stockout": stockout,
            },
            "low_stock_products": low_stock_products,
        }

class ButtonGroupManager:
    def __init__(self):
        self.selected_button = None

    def select(self, button):
        if self.selected_button and self.selected_button is not button:
            self.selected_button.deselect()
        self.selected_button = button
        button.set_selected(True)
class CustomButton(QPushButton):
    def __init__(self, text, parent, normal_color, hover_color, click_color, group_manager, text_color="black",
                 font_size=14):
        super().__init__(text, parent)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text_color = text_color
        self.font_size = font_size
        self.group_manager = group_manager
        self.selected = False
        self.setStyleSheet(
            f"background-color: {self.normal_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        self._hovered = False

    def enterEvent(self, event):
        if not self.selected:
            self.setStyleSheet(
                f"background-color: {self.hover_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        self._hovered = True

    def leaveEvent(self, event):
        if not self.selected:
            self.setStyleSheet(
                f"background-color: {self.normal_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        self._hovered = False

    def mousePressEvent(self, event):
        self.group_manager.select(self)
        super().mousePressEvent(event)

    def set_selected(self, selected):
        self.selected = selected
        if selected:
            self.setStyleSheet(
                f"background-color: {self.click_color}; color: {self.text_color}; font-size: {self.font_size}px;")
        else:
            self.setStyleSheet(
                f"background-color: {self.normal_color}; color: {self.text_color}; font-size: {self.font_size}px;")

    def deselect(self):
        self.set_selected(False)

class AdminDashboard(QWidget):
    def __init__(self, login_widget, username, conn):
        super().__init__()
        self.login_widget = login_widget
        self.username = username
        self.conn = conn


        self.setWindowTitle("Admin")
        self.setWindowIcon(QIcon("images/compforgelogobgremoved.png"))
        self.setGeometry(10, 35, 1350, 650)
        self.setFixedSize(1350, 650)
        self.setStyleSheet("background-color:rgb( 40, 40, 40); border-radius: 10px;")

        self.dashboard_panel = None
        self.reports_panel = None
        self.users_panel = None
        self.logs_panel = None

        self.buttonPanel = QWidget(self)
        self.buttonPanel.setGeometry(10, 10, 160, 630)
        self.buttonPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.buttonPanel.show()

        image_widget = QLabel(self.buttonPanel)
        image_widget.setGeometry(20, 5, 120, 120)
        logo = QPixmap("images/compforgelogobgremoved.png")
        image_widget.setPixmap(logo)
        image_widget.setScaledContents(True)
        image_widget.show()

        self.button_group = ButtonGroupManager()

        self.dashboard_btn = CustomButton(
            "Dashboard", self.buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group)
        self.dashboard_btn.setGeometry(20, 150, 120, 40)
        self.dashboard_btn.clicked.connect(self.show_dashboard_panel)

        self.reports_btn = CustomButton(
            "Reports", self.buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group)
        self.reports_btn.setGeometry(20, 230, 120, 40)
        self.reports_btn.clicked.connect(self.show_reports_panel)

        self.users_btn = CustomButton(
            "Users", self.buttonPanel,
            "rgb(60, 146, 193)", "cyan", "cyan", self.button_group)
        self.users_btn.setGeometry(20, 310, 120, 40)
        self.users_btn.clicked.connect(self.show_users_panel)

        self.back_btn = CustomButton(
            "←", self.buttonPanel,
            "rgb(70, 70, 70)", "rgb(40,40,40)", "rgb(40,40,40)", self.button_group,
            text_color="rgb(60, 146, 193)", font_size=40)
        self.back_btn.setGeometry(20, 580, 50, 40)
        self.back_btn.mousePressEvent = self.handle_back_btn_click

        self.topPanel = QWidget(self)
        self.topPanel.setGeometry(180, 10, 1160, 100)
        self.topPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.topPanel.show()

        self.analyticPanel = QWidget(self)
        self.analyticPanel.setGeometry(180, 120, 1160, 520)
        self.analyticPanel.setStyleSheet("background-color: rgb(70, 70, 70)")
        self.analyticPanel.show()
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT fname, lname FROM accounts WHERE username=%s",
                (self.username,)
            )
            result = cursor.fetchone()
            cursor.close()

            if result:
                fname, lname = result
                title_label = QLabel(f"CompForge Inventory Admin: {fname} {lname}", self.topPanel)
                title_label.setGeometry(20, 30, 600, 40)
                title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
                title_label.show()
            else:
                QMessageBox.information(self, "Account Details", "Account details not found.")
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

        # --- Analytic Panel ---
        self.analyticPanel = QWidget(self)
        self.analyticPanel.setGeometry(180, 120, 1160, 520)
        self.analyticPanel.setStyleSheet("background-color: rgb(70, 70, 70)")

        self.show_dashboard_panel()

    def hide_all_panels(self):
        for panel in [self.dashboard_panel, self.reports_panel, self.users_panel]:
            if panel:
                panel.hide()

    def show_dashboard_panel(self):
        self.hide_all_panels()
        if not self.dashboard_panel:
            self.dashboard_panel = DashboardPanel(self.conn, self.analyticPanel)
        self.dashboard_panel.show()

    def show_reports_panel(self):
        self.hide_all_panels()

        if not hasattr(self, 'reports_panel') or self.reports_panel is None:
            self.reports_panel = QWidget(self.analyticPanel)
            self.reports_panel.setGeometry(10, 10, 1140, 500)
            self.reports_panel.setStyleSheet("background-color: rgb(100, 100, 100); border-radius: 10px;")

            # Header
            header_label = QLabel("Reports Overview", self.reports_panel)
            header_label.setGeometry(20, 10, 400, 40)
            header_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")

            # Table Style
            table_style = """
                QTableWidget {
                    background-color: #f8f9fa;
                    alternate-background-color: #e9ecef;
                    gridline-color: #b0b0b0;
                    border-radius: 10px;
                    font-size: 13px;
                    selection-background-color: rgb(70,130,250);
                    selection-color: white;
                }
                QHeaderView::section {
                    background-color: rgb(50,150,200);
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 6px;
                }
            """

            # --- Stock In Section ---
            stockin_label = QLabel("Stock Ins", self.reports_panel)
            stockin_label.setGeometry(20, 60, 200, 30)
            stockin_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

            # Table for Stock In
            self.stockin_table = QTableWidget(self.reports_panel)
            self.stockin_table.setGeometry(20, 100, 1100, 160)
            self.stockin_table.setColumnCount(8)
            self.stockin_table.setHorizontalHeaderLabels([
                "ID", "ProductID", "ProductName", "Supplier", "Price", "Quantity", "Total", "Stocked By"
            ])
            self.stockin_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.stockin_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.stockin_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.stockin_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.stockin_table.verticalHeader().setVisible(False)
            self.stockin_table.setStyleSheet(table_style)

            # --- Stock Out Section ---
            stockout_label = QLabel("Stock Outs", self.reports_panel)
            stockout_label.setGeometry(20, 280, 200, 30)
            stockout_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")

            # Refresh button
            refresh_btn = QPushButton("↻ Refresh", self.reports_panel)
            refresh_btn.setGeometry(950, 280, 150, 30)
            refresh_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgb(50,150,200);
                    color: white;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(70,170,220);
                }
            """)
            refresh_btn.clicked.connect(self.load_reports_data)

            # Table for Stock Out
            self.stockout_table = QTableWidget(self.reports_panel)
            self.stockout_table.setGeometry(20, 320, 1100, 160)
            self.stockout_table.setColumnCount(8)
            self.stockout_table.setHorizontalHeaderLabels([
                "ID", "ProductID", "ProductName", "Supplier", "Price", "Quantity", "Total", "Stocked By"
            ])
            self.stockout_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.stockout_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.stockout_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.stockout_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.stockout_table.verticalHeader().setVisible(False)
            self.stockout_table.setStyleSheet(table_style)

            # Load initial data
            self.load_reports_data()

        self.reports_panel.show()

    def load_reports_data(self):
        """Loads stock in and stock out data into tables."""
        try:
            cursor = self.conn.cursor()
            # --- Load Stock In Data ---
            cursor.execute("""
                           SELECT s.StockInID,
                                  p.ProductID,
                                  p.ProductName,
                                  sup.SupplierName,
                                  p.Price,
                                  s.Quantity                    AS QuantityAdded,
                                  (p.Price * s.Quantity)        AS Total,
                                  CONCAT(a.FName, ' ', a.LName) AS StockedBy
                           FROM stockin s
                                    JOIN products p ON s.ProductID = p.ProductID
                                    JOIN suppliers sup ON p.SupplierID = sup.SupplierID
                                    JOIN accounts a ON s.AccountID = a.AccountID
                           ORDER BY s.StockInID DESC
                           """)
            stockins = cursor.fetchall()
            self.stockin_table.setRowCount(0)
            for row_data in stockins:
                row_idx = self.stockin_table.rowCount()
                self.stockin_table.insertRow(row_idx)
                for col, data in enumerate(row_data):
                    self.stockin_table.setItem(row_idx, col, QTableWidgetItem(str(data)))

            # --- Load Stock Out Data ---
            cursor.execute("""
                           SELECT s.StockOutID,
                                  p.ProductID,
                                  p.ProductName,
                                  sup.SupplierName,
                                  p.Price,
                                  s.Quantity                    AS QuantityRemoved,
                                  (p.Price * s.Quantity)        AS Total,
                                  CONCAT(a.FName, ' ', a.LName) AS StockedBy
                           FROM stockout s
                                    JOIN products p ON s.ProductID = p.ProductID
                                    JOIN suppliers sup ON p.SupplierID = sup.SupplierID
                                    JOIN accounts a ON s.AccountID = a.AccountID
                           ORDER BY s.StockOutID DESC
                           """)
            stockouts = cursor.fetchall()
            self.stockout_table.setRowCount(0)
            for row_data in stockouts:
                row_idx = self.stockout_table.rowCount()
                self.stockout_table.insertRow(row_idx)
                for col, data in enumerate(row_data):
                    self.stockout_table.setItem(row_idx, col, QTableWidgetItem(str(data)))

            cursor.close()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def show_users_panel(self):
        self.hide_all_panels()

        if not hasattr(self, "users_panel") or self.users_panel is None:
            self.users_panel = QWidget(self.analyticPanel)
            self.users_panel.setGeometry(10, 10, 1140, 500)
            self.users_panel.setStyleSheet("background-color: rgb(100, 100, 100); border-radius: 10px;")

            # Title
            label = QLabel("Users Overview", self.users_panel)
            label.setGeometry(20, 10, 400, 40)
            label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

            # Table setup
            self.users_table = QTableWidget(self.users_panel)
            self.users_table.setGeometry(20, 60, 900, 400)
            self.users_table.setColumnCount(5)
            self.users_table.setHorizontalHeaderLabels(["AccountID", "Username", "Password", "Role", "Full Name"])
            self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.users_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.users_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.users_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.users_table.verticalHeader().setVisible(False)
            self.users_table.setStyleSheet("""
                QTableWidget {
                    background-color: #f8f9fa;
                    alternate-background-color: #e9ecef;
                    gridline-color: #b0b0b0;
                    border-radius: 10px;
                    font-size: 13px;
                    selection-background-color: rgb(70,130,250);
                    selection-color: white;
                }
                QHeaderView::section {
                    background-color: rgb(50,150,200);
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 6px;
                }
            """)

            # Buttons
            add_btn = QPushButton("Add Account", self.users_panel)
            add_btn.setGeometry(940, 100, 160, 40)
            add_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(50,150,200);
                        color: white;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: rgb(70,170,220);
                    }
                    QPushButton:pressed {
                        background-color: rgb(30,130,180);
                    }
                """)
            add_btn.clicked.connect(self.add_account)

            update_btn = QPushButton("Update Account", self.users_panel)
            update_btn.setGeometry(940, 160, 160, 40)
            update_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(50,150,200);
                        color: white;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: rgb(70,170,220);
                    }
                    QPushButton:pressed {
                        background-color: rgb(30,130,180);
                    }
                """)
            update_btn.clicked.connect(self.update_account)

            delete_btn = QPushButton("Delete Account", self.users_panel)
            delete_btn.setGeometry(940, 220, 160, 40)
            delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(50,150,200);
                        color: white;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: rgb(70,170,220);
                    }
                    QPushButton:pressed {
                        background-color: rgb(30,130,180);
                    }
                """)
            delete_btn.clicked.connect(self.delete_account)

            refresh_btn = QPushButton("Refresh", self.users_panel)
            refresh_btn.setGeometry(940, 280, 160, 40)
            refresh_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(50,150,200);
                        color: white;
                        border-radius: 8px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: rgb(70,170,220);
                    }
                    QPushButton:pressed {
                        background-color: rgb(30,130,180);
                    }
                """)
            refresh_btn.clicked.connect(self.load_users_data)

            # Load data
            self.load_users_data()

        self.users_panel.show()

    def load_users_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                           SELECT AccountID, Username, Password, Role, CONCAT(FName, ' ', LName) AS FullName
                           FROM accounts
                           ORDER BY AccountID ASC
                           """)
            users = cursor.fetchall()
            cursor.close()

            self.users_table.setRowCount(0)
            for row_data in users:
                row_idx = self.users_table.rowCount()
                self.users_table.insertRow(row_idx)
                for col, data in enumerate(row_data):
                    self.users_table.setItem(row_idx, col, QTableWidgetItem(str(data)))

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def add_account(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Account")
        dialog.setFixedSize(400, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: rgb(70,70,70);
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                background-color: transparent;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid rgb(120,120,120);
                border-radius: 10px;
                padding: 4px;
                font-size: 13px;
                color: black;
            }
            QComboBox {
                background-color: rgb(100, 100, 100);
                border: 1px solid rgb(120,120,120);
                border-radius: 10px;
                padding: 4px;
                font-size: 13px;
                color: black;
            }
            QComboBox QAbstractItemView {               
                background-color: rgb(255,255,255);    
                selection-background-color: rgb(70,130,250);  
                selection-color: white;                 
                color: black;                            
                border-radius: 6px;
            }
            QLineEdit:focus {
                border: 1px solid rgb(70,130,250);
                background-color: white;
            }
            QComboBox:focus {
                border: 1px solid rgb(70,130,250);
                background-color: rgb(100, 100, 100);
            }
            QPushButton {
                background-color: rgb(50,150,200);
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: rgb(70,170,220);
            }
            QPushButton:pressed {
                background-color: rgb(30,130,180);
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)

        # === Input Fields ===
        username_label = QLabel("Username:")
        username_input = QLineEdit()

        password_label = QLabel("Password:")
        password_input = QLineEdit()

        fname_label = QLabel("First Name:")
        fname_input = QLineEdit()

        lname_label = QLabel("Last Name:")
        lname_input = QLineEdit()

        role_label = QLabel("Role:")
        role_combo = QComboBox()
        role_combo.addItems(["Admin", "Staff"])

        # === Buttons ===
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Account")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(cancel_btn)
        cancel_btn.clicked.connect(dialog.reject)

        # === Add Widgets to Layout ===
        layout.addWidget(username_label)
        layout.addWidget(username_input)
        layout.addWidget(password_label)
        layout.addWidget(password_input)
        layout.addWidget(fname_label)
        layout.addWidget(fname_input)
        layout.addWidget(lname_label)
        layout.addWidget(lname_input)
        layout.addWidget(role_label)
        layout.addWidget(role_combo)
        layout.addLayout(btn_layout)

        # === Add Account Logic ===
        def save():
            username = username_input.text().strip()
            password = password_input.text().strip()
            fname = fname_input.text().strip()
            lname = lname_input.text().strip()
            role = role_combo.currentText()

            if not all([username, password, fname, lname]):
                QMessageBox.warning(dialog, "Input Error", "All fields are required.")
                return

            if len(password) < 8:
                QMessageBox.warning(dialog, "Weak Password", "Password must be at least 8 characters long.")
                return

            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                               INSERT INTO accounts (Username, Password, FName, LName, Role)
                               VALUES (%s, %s, %s, %s, %s)
                               """, (username, password, fname, lname, role))
                self.conn.commit()
                cursor.close()

                QMessageBox.information(dialog, "Success", "Account added successfully.")
                self.load_users_data()
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(dialog, "Database Error", str(e))

        add_btn.clicked.connect(save)
        dialog.exec()

    def update_account(self):
        selected = self.users_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selection Error", "Please select an account to update.")
            return

        account_id = self.users_table.item(selected, 0).text()
        username = self.users_table.item(selected, 1).text()
        password = self.users_table.item(selected, 2).text()
        role = self.users_table.item(selected, 3).text()
        fullname = self.users_table.item(selected, 4).text().split(" ")
        fname = fullname[0]
        lname = fullname[1] if len(fullname) > 1 else ""

        dialog = QDialog(self)
        dialog.setWindowTitle("Update Account")
        dialog.setFixedSize(400, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: rgb(70,70,70);
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                background-color: transparent;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid rgb(120,120,120);
                border-radius: 10px;
                padding: 4px;
                font-size: 13px;
                color: black;
            }
            QComboBox {
                background-color: rgb(100, 100, 100);
                border: 1px solid rgb(120,120,120);
                border-radius: 10px;
                padding: 4px;
                font-size: 13px;
                color: black;
            }
            QComboBox QAbstractItemView {               
                background-color: rgb(255,255,255);    
                selection-background-color: rgb(70,130,250);  
                selection-color: white;                 
                color: black;                            
                border-radius: 6px;
            }
            QLineEdit:focus {
                border: 1px solid rgb(70,130,250);
                background-color: white;
            }
            QComboBox:focus {
                border: 1px solid rgb(70,130,250);
                background-color: rgb(100, 100, 100);
            }
            QPushButton {
                background-color: rgb(50,150,200);
                color: white;
                font-weight: bold;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: rgb(70,170,220);
            }
            QPushButton:pressed {
                background-color: rgb(30,130,180);
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)

        # === Input Fields ===
        username_label = QLabel("Username:")
        username_input = QLineEdit(username)

        password_label = QLabel("Password:")
        password_input = QLineEdit(password)

        fname_label = QLabel("First Name:")
        fname_input = QLineEdit(fname)

        lname_label = QLabel("Last Name:")
        lname_input = QLineEdit(lname)

        role_label = QLabel("Role:")
        role_combo = QComboBox()
        role_combo.addItems(["Admin", "Staff"])
        role_combo.setCurrentText(role)

        # === Buttons ===
        btn_layout = QHBoxLayout()
        update_btn = QPushButton("Update Account")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(update_btn)
        btn_layout.addWidget(cancel_btn)
        cancel_btn.clicked.connect(dialog.reject)

        # === Add Widgets to Layout ===
        layout.addWidget(username_label)
        layout.addWidget(username_input)
        layout.addWidget(password_label)
        layout.addWidget(password_input)
        layout.addWidget(fname_label)
        layout.addWidget(fname_input)
        layout.addWidget(lname_label)
        layout.addWidget(lname_input)
        layout.addWidget(role_label)
        layout.addWidget(role_combo)
        layout.addLayout(btn_layout)

        # === Update Account Logic ===
        def save():
            new_username = username_input.text().strip()
            new_password = password_input.text().strip()
            new_fname = fname_input.text().strip()
            new_lname = lname_input.text().strip()
            new_role = role_combo.currentText()

            if not all([new_username, new_password, new_fname, new_lname]):
                QMessageBox.warning(dialog, "Input Error", "All fields are required.")
                return

            if len(new_password) < 8:
                QMessageBox.warning(dialog, "Weak Password", "Password must be at least 8 characters long.")
                return

            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                               UPDATE accounts
                               SET Username=%s,
                                   Password=%s,
                                   FName=%s,
                                   LName=%s,
                                   Role=%s
                               WHERE AccountID = %s
                               """, (new_username, new_password, new_fname, new_lname, new_role, account_id))
                self.conn.commit()
                cursor.close()

                QMessageBox.information(dialog, "Success", "Account updated successfully.")
                self.load_users_data()
                dialog.accept()
            except Exception as e:
                QMessageBox.critical(dialog, "Database Error", str(e))

        update_btn.clicked.connect(save)
        dialog.exec()

    def delete_account(self):
        selected = self.users_table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Selection Error", "Please select an account to delete.")
            return

        account_uname = self.users_table.item(selected, 1).text()

        confirm = QMessageBox.question(
            self, "Confirm Deletion", f"Are you sure you want to delete {account_uname}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.No:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM accounts WHERE AccountID=%s", (account_id,))
            self.conn.commit()
            cursor.close()

            QMessageBox.information(self, "Deleted", "Account deleted successfully.")
            self.load_users_data()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def handle_back_btn_click(self, event):
        reply = QMessageBox.question(
            self, "Logout?", "Logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            self.login_widget.setVisible(True)


