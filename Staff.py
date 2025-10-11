from PyQt6.QtCore import QDateTime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
from IMS import *

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

        # Store widgets for refresh later
        self.summary_layout = QHBoxLayout()
        self.graph_layout = QHBoxLayout()

        self.main_layout.addLayout(self.summary_layout)
        self.main_layout.addLayout(self.graph_layout)

        low_stock_header = QHBoxLayout()
        self.low_stock_label = QLabel("Low Stock Products")
        self.low_stock_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self.low_stock_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        low_stock_header.addWidget(self.low_stock_label)

        # Refresh button
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

        # Create low stock table
        self.low_stock_table = QTableWidget()
        self.low_stock_table.setColumnCount(4)
        self.low_stock_table.setHorizontalHeaderLabels(["Product Name", "Type", "Quantity", "Reorder Level"])
        self.low_stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.low_stock_table.verticalHeader().setVisible(False)
        self.low_stock_table.setStyleSheet("""
            QTableWidget {
                color: black;
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

        # Update Low Stock Table
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
class StaffDashboard(QWidget):
    def __init__(self, login_widget, username, conn):
        super().__init__()
        self.login_widget = login_widget
        self.username = username
        self.conn = conn

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT AccountID FROM accounts WHERE UserName=%s", (self.username,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                self.current_user_id = result[0]
            else:
                self.current_user_id = None
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
            self.current_user_id = None

        self.setWindowTitle("Staff")
        self.setWindowIcon(QIcon("images/compforgelogobgremoved.png"))
        self.setGeometry(10, 35, 1350, 650)
        self.setFixedSize(1350, 650)
        self.setStyleSheet("background-color:rgb(40, 40, 40); border-radius: 10px;")

        # ===== PANELS =====
        self.account_panel = None
        self.dashboard_panel = None
        self.inventory_panel = None
        self.category_panel = None
        self.history_panel = None

        # --- Button Panel ---
        self.buttonPanel = QWidget(self)
        self.buttonPanel.setGeometry(10, 10, 160, 630)
        self.buttonPanel.setStyleSheet("background-color: rgb(70, 70, 70)")

        image_widget = QLabel(self.buttonPanel)
        image_widget.setGeometry(20, 5, 120, 120)
        logo = QPixmap("images/compforgelogobgremoved.png")
        image_widget.setPixmap(logo)
        image_widget.setScaledContents(True)

        self.button_group = ButtonGroupManager()

        # --- Buttons ---
        self.dashboard_btn = CustomButton("Dashboard", self.buttonPanel,
                                          "rgb(60, 146, 193)", "cyan", "cyan", self.button_group)
        self.dashboard_btn.setGeometry(20, 150, 120, 40)
        self.dashboard_btn.clicked.connect(self.show_dashboard_panel)

        self.inventory_btn = CustomButton("Inventory", self.buttonPanel,
                                          "rgb(60, 146, 193)", "cyan", "cyan", self.button_group)
        self.inventory_btn.setGeometry(20, 230, 120, 40)
        self.inventory_btn.clicked.connect(self.show_inventory_panel)

        self.category_btn = CustomButton("Category", self.buttonPanel,
                                         "rgb(60, 146, 193)", "cyan", "cyan", self.button_group)
        self.category_btn.setGeometry(20, 310, 120, 40)
        self.category_btn.clicked.connect(self.show_category_panel)


        self.account_btn = CustomButton("Account", self.buttonPanel,
                                        "rgb(60, 146, 193)", "cyan", "cyan", self.button_group)
        self.account_btn.setGeometry(20, 390, 120, 40)
        self.account_btn.clicked.connect(self.show_account_panel)

        self.back_btn = CustomButton("←", self.buttonPanel,
                                     "rgb(70, 70, 70)", "rgb(40,40,40)", "rgb(40,40,40)",
                                     self.button_group, text_color="rgb(60, 146, 193)", font_size=40)
        self.back_btn.setGeometry(20, 580, 50, 40)
        self.back_btn.clicked.connect(self.handle_back_btn_click)

        # --- Top Panel ---
        self.topPanel = QWidget(self)
        self.topPanel.setGeometry(180, 10, 1160, 100)
        self.topPanel.setStyleSheet("background-color: rgb(70, 70, 70)")


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
                title_label = QLabel(f"CompForge Inventory Staff: {fname} {lname}", self.topPanel)
                title_label.setGeometry(20, 30, 500, 40)
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
    # ==========================
    # Hide all panels
    # ==========================
    def hide_all_panels(self):
        for panel in [self.dashboard_panel, self.inventory_panel, self.category_panel,
                      self.history_panel, self.account_panel]:
            if panel:
                panel.hide()

    # ==========================
    # Panel Functions
    # ==========================
    def show_dashboard_panel(self):
        self.hide_all_panels()
        if not self.dashboard_panel:
            self.dashboard_panel = DashboardPanel(self.conn, self.analyticPanel)
        self.dashboard_panel.show()

    def show_inventory_panel(self):
        self.hide_all_panels()

        if not self.inventory_panel:
            self.inventory_panel = QWidget(self.analyticPanel)
            self.inventory_panel.setGeometry(10, 10, 1140, 500)
            self.inventory_panel.setStyleSheet("background-color: rgb(100, 100, 100); border-radius: 10px;")

            title = QLabel("Inventory Management", self.inventory_panel)
            title.setGeometry(20, 10, 400, 40)
            title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")

            # Search bar
            self.search_bar = QLineEdit(self.inventory_panel)
            self.search_bar.setPlaceholderText("Search product name...")
            self.search_bar.setStyleSheet("""
                QLineEdit {
                    background-color: white;
                    color: black;
                    border: 2px solid rgb(100, 100, 100);
                    border-radius: 8px;
                    padding-left: 10px;
                    font-size: 14px;
                }
                QLineEdit:hover {
                    border: 2px solid rgb(100, 150, 250);
                }
                QLineEdit:focus {
                    border: 2px solid rgb(70, 130, 250);
                    background-color: white;
                }
                QMessageBox {
                    background-color: rgb(40,40,40);
                    color: white;
                    font-size: 14px;
                }
                QMessageBox QLabel {
                    color: white;
                }
                
            """)
            self.search_bar.setGeometry(100, 60, 200, 30)
            self.search_bar.textChanged.connect(self.search_product)

            self.search_btn = QPushButton("Search:", self.inventory_panel)
            self.search_btn.setGeometry(20, 60, 80, 30)
            self.search_btn.setStyleSheet("color: white; font-size: 14px")
            self.search_btn.clicked.connect(self.search_product)

            # Table setup
            self.table = QTableWidget(self.inventory_panel)
            self.table.setGeometry(20, 100, 1100, 350)
            # Table setup
            self.table.setColumnCount(9)
            self.table.setHorizontalHeaderLabels([
                "ProductID", "ProductName", "Type", "Supplier",
                "Price", "Stock", "Total", "ReorderLevel", "DateSupplied"
            ])
            self.table.setColumnWidth(1, 200)
            self.table.setStyleSheet("""
                QTableWidget {
                    color: black;
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
                QHeaderView::section:first {
                    border-top-left-radius: 10px;
                }

                /* Rightmost header cell */
                QHeaderView::section:last {
                    border-top-right-radius: 10px;
                }

                QTableCornerButton::section {
                    background-color: rgb(50,150,200);
                    border: none;
                }

                /* ===== Vertical Scrollbar ===== */
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

                /* ===== Horizontal Scrollbar (bottom) ===== */
                QScrollBar:horizontal {
                    background: #e2e2e2;
                    height: 10px;
                    margin: 0 2px 0 2px;
                    border-radius: 5px;
                }
                QScrollBar::handle:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb(130,180,230), stop:1 rgb(90,150,210));
                    border-radius: 20px;
                    min-width: 20px;
                }
                QScrollBar::handle:horizontal:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb(150,200,250), stop:1 rgb(100,160,220));
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    width: 0px;
                    background: none;
                }
                QMessageBox {
                    background-color: rgb(40,40,40);
                    color: white;
                    font-size: 14px;
                }
                QMessageBox QLabel {
                    color: white;
                }
            """)
            self.table.setAlternatingRowColors(True)
            self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.table.horizontalHeader().setStretchLastSection(True)
            self.table.verticalHeader().setVisible(False)

            # CRUD Buttons
            # self.add_btn = QPushButton("Add", self.inventory_panel)
            # self.add_btn.setGeometry(20, 460, 150, 30)
            # self.add_btn.clicked.connect(self.add_product)
            #
            # self.update_btn = QPushButton("Update", self.inventory_panel)
            # self.update_btn.setGeometry(185, 460, 150, 30)
            # self.update_btn.clicked.connect(self.update_product)
            #
            # self.delete_btn = QPushButton("Delete", self.inventory_panel)
            # self.delete_btn.setGeometry(350, 460, 150, 30)
            # self.delete_btn.clicked.connect(self.delete_product)

            self.stock_in_btn = QPushButton("Stock In", self.inventory_panel)
            self.stock_in_btn.setGeometry(330, 60, 150, 30)
            self.stock_in_btn.clicked.connect(self.stock_in)

            self.stock_out_btn = QPushButton("Stock Out", self.inventory_panel)
            self.stock_out_btn.setGeometry(500, 60, 150, 30)
            self.stock_out_btn.clicked.connect(self.stock_out)

            # Shared button style
            for btn in [
                self.stock_in_btn,
                self.stock_out_btn,
            ]:
                btn.setStyleSheet("""
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
                    QMessageBox {
                        background-color: rgb(40,40,40);
                        color: white;
                        font-size: 14px;
                    }
                    QMessageBox QLabel {
                        color: white;
                    }
                """)

            self.load_products()

        self.inventory_panel.show()

        # -----------------------------------------------------
        # LOAD PRODUCTS FROM DATABASE
        # -----------------------------------------------------

    def load_products(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                       SELECT p.ProductID,
                              p.ProductName,
                              t.TypeName,
                              s.SupplierName,
                              p.Price,
                              p.Quantity,
                              p.Total,
                              p.ReorderLevel,
                              p.DateSupplied
                       FROM products AS p
                                LEFT JOIN type AS t ON p.TypeID = t.TypeID
                                LEFT JOIN suppliers AS s ON p.SupplierID = s.SupplierID
                       """)
        rows = cursor.fetchall()
        cursor.close()

        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels([
            "Product ID", "Product Name", "Type", "Supplier",
            "Price", "Stock", "Total", "Reorder Level", "Date Supplied"
        ])

        for row_data in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for column, data in enumerate(row_data):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

        # -----------------------------------------------------
        # SEARCH PRODUCT
        # -----------------------------------------------------

    def search_product(self):
        keyword = self.search_bar.text().strip()

        # If search bar is empty, reload all products
        if keyword == "":
            self.load_products()
            return

        cursor = self.conn.cursor()
        query = """
                SELECT p.ProductID, \
                       p.ProductName, \
                       t.TypeName, \
                       s.SupplierName, \
                       p.Price, \
                       p.Quantity, \
                       p.Total, \
                       p.ReorderLevel
                FROM products AS p
                         LEFT JOIN type AS t ON p.TypeID = t.TypeID
                         LEFT JOIN suppliers AS s ON p.SupplierID = s.SupplierID
                WHERE CAST(p.ProductID AS CHAR) LIKE %s
                   OR p.ProductName LIKE %s
                   OR t.TypeName LIKE %s
                   OR s.SupplierName LIKE %s \
                """
        # We use CAST(ProductID AS CHAR) so we can search it as text
        cursor.execute(query, (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        ))
        rows = cursor.fetchall()
        cursor.close()

        # Clear table and show results
        self.table.setRowCount(0)
        for row_data in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for column, data in enumerate(row_data):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))

        # -----------------------------------------------------
        # ADD PRODUCT (placeholder)
        # -----------------------------------------------------

    # def add_product(self):
    #     dialog = QDialog(self)
    #     dialog.setWindowTitle("Add New Product")
    #     dialog.setFixedSize(400, 600)
    #     dialog.setStyleSheet("""
    #         QDialog {
    #             background-color: rgb(70,70,70);
    #             border-radius: 10px;
    #         }
    #         QLabel {
    #             font-size: 14px;
    #             font-weight: bold;
    #             color: white;
    #             background-color: transparent;
    #         }
    #         QLineEdit {
    #             background-color: white;
    #             border: 1px solid rgb(120,120,120);
    #             border-radius: 10px;
    #             padding: 4px;
    #             font-size: 13px;
    #             color: black;
    #         }
    #         QComboBox {
    #             background-color: rgb(100, 100, 100);
    #             border: 1px solid rgb(120,120,120);
    #             border-radius: 10px;
    #             padding: 4px;
    #             font-size: 13px;
    #             color: black;
    #         }
    #         QComboBox QAbstractItemView {
    #             background-color: rgb(255,255,255);
    #             selection-background-color: rgb(70,130,250);
    #             selection-color: white;
    #             color: black;
    #             border-radius: 6px;
    #         }
    #         QLineEdit:focus {
    #             border: 1px solid rgb(70,130,250);
    #             background-color: white;
    #         }
    #         QComboBox:focus {
    #             border: 1px solid rgb(70,130,250);
    #             background-color: rgb(100, 100, 100);
    #         }
    #         QPushButton {
    #             background-color: rgb(50,150,200);
    #             color: white;
    #             font-weight: bold;
    #             border-radius: 6px;
    #             padding: 6px;
    #         }
    #         QPushButton:hover {
    #             background-color: rgb(70,170,220);
    #         }
    #         QPushButton:pressed {
    #             background-color: rgb(30,130,180);
    #         }
    #         QMessageBox {
    #             background-color: rgb(40,40,40);
    #             color: white;
    #             font-size: 14px;
    #         }
    #         QMessageBox QLabel {
    #             color: white;
    #         }
    #     """)
    #
    #     layout = QVBoxLayout(dialog)
    #     layout.setSpacing(10)
    #
    #     # === Input Fields ===
    #     name_label = QLabel("Product Name:")
    #     name_input = QLineEdit()
    #
    #     price_label = QLabel("Price:")
    #     price_input = QLineEdit()
    #     price_input.setPlaceholderText("Enter price (e.g., 99.99)")
    #
    #     quantity_label = QLabel("Quantity:")
    #     quantity_input = QLineEdit()
    #     quantity_input.setPlaceholderText("Enter quantity (e.g., 10)")
    #
    #     total_label = QLabel("Total:")
    #     total_input = QLineEdit()
    #     total_input.setReadOnly(True)
    #     total_input.setStyleSheet("background-color: rgb(200,200,200); color: #333; border-radius: 6px;")
    #
    #     reorder_label = QLabel("Reorder Level:")
    #     reorder_input = QLineEdit()
    #     reorder_input.setPlaceholderText("Enter reorder level (e.g., 5)")
    #
    #     type_label = QLabel("Type:")
    #     type_combo = QComboBox()
    #
    #     supplier_label = QLabel("Supplier:")
    #     supplier_input = QLineEdit()
    #     supplier_input.setPlaceholderText("Enter supplier name")
    #
    #     # cursor = self.conn.cursor()
    #     # cursor.execute("SELECT TypeID, TypeName FROM type")
    #     # for tid, tname in cursor.fetchall():
    #     #     type_combo.addItem(tname, tid)
    #
    #     # Load dropdowns from DB
    #     try:
    #         cursor = self.conn.cursor()
    #         cursor.execute("SELECT TypeID, TypeName FROM type")
    #         for tid, tname in cursor.fetchall():
    #             type_combo.addItem(tname, tid)
    #
    #     except Exception as e:
    #         QMessageBox.critical(dialog, "Database Error", f"Failed to check/insert supplier:\n{str(e)}")
    #         return
    #
    #     # === Auto calculate total ===
    #     def calculate_total():
    #         try:
    #             price = float(price_input.text()) if price_input.text() else 0
    #             qty = int(quantity_input.text()) if quantity_input.text() else 0
    #             total_input.setText(f"{price * qty:.2f}")
    #         except ValueError:
    #             total_input.setText("")
    #
    #     price_input.textChanged.connect(calculate_total)
    #     quantity_input.textChanged.connect(calculate_total)
    #
    #     # === Buttons ===
    #     btn_layout = QHBoxLayout()
    #     add_btn = QPushButton("Add Product")
    #     cancel_btn = QPushButton("Cancel")
    #     btn_layout.addWidget(add_btn)
    #     btn_layout.addWidget(cancel_btn)
    #     cancel_btn.clicked.connect(dialog.reject)
    #
    #     # === Add Widgets to Layout ===
    #     layout.addWidget(name_label)
    #     layout.addWidget(name_input)
    #     layout.addWidget(price_label)
    #     layout.addWidget(price_input)
    #     layout.addWidget(quantity_label)
    #     layout.addWidget(quantity_input)
    #     layout.addWidget(total_label)
    #     layout.addWidget(total_input)
    #     layout.addWidget(reorder_label)
    #     layout.addWidget(reorder_input)
    #     layout.addWidget(type_label)
    #     layout.addWidget(type_combo)
    #     layout.addWidget(supplier_label)
    #     layout.addWidget(supplier_input)
    #     layout.addLayout(btn_layout)
    #
    #     # === Add Product Logic ===
    #     def save_product():
    #         name = name_input.text().strip()
    #         price = price_input.text().strip()
    #         quantity = quantity_input.text().strip()
    #         total = total_input.text().strip()
    #         reorder = reorder_input.text().strip()
    #         type_id = type_combo.currentData()
    #         supplier_name = supplier_input.text().strip()
    #         if not supplier_name:
    #             QMessageBox.warning(dialog, "Input Error", "Supplier name is required.")
    #             return
    #
    #         # Check if supplier exists
    #         try:
    #             cursor = self.conn.cursor()
    #             cursor.execute("SELECT SupplierID FROM suppliers WHERE SupplierName=%s", (supplier_name,))
    #             result = cursor.fetchone()
    #
    #             if result:
    #                 supplier_id = result[0]  # existing supplier
    #             else:
    #                 # Insert new supplier
    #                 cursor.execute("INSERT INTO suppliers (SupplierName) VALUES (%s)", (supplier_name,))
    #                 self.conn.commit()
    #                 supplier_id = cursor.lastrowid  # get the newly inserted SupplierID
    #
    #             cursor.close()
    #         except Exception as e:
    #             QMessageBox.critical(dialog, "Database Error", f"Failed to check/insert supplier:\n{str(e)}")
    #             return
    #         date_supplied = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #
    #         # Validation
    #         if not all([name, price, quantity, total, reorder]):
    #             QMessageBox.warning(dialog, "Input Error", "All fields are required.")
    #             return
    #         try:
    #             price = float(price)
    #             quantity = int(quantity)
    #             total = float(total)
    #             reorder = int(reorder)
    #         except ValueError:
    #             QMessageBox.warning(dialog, "Input Error", "Price, Quantity, and Reorder Level must be numeric.")
    #             return
    #
    #         # Confirmation box
    #         confirm = QMessageBox.question(
    #             dialog,
    #             "Confirm Add Product",
    #             f"Are you sure you want to add this product?\n\n"
    #             f"Name: {name}\nPrice: {price}\nQuantity: {quantity}\n"
    #             f"Total: {total}\nReorder Level: {reorder}",
    #             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    #         )
    #
    #         if confirm != QMessageBox.StandardButton.Yes:
    #             return  # user cancelled
    #
    #         # Insert into DB
    #         try:
    #             cursor = self.conn.cursor()
    #             cursor.execute("""
    #                            INSERT INTO products (ProductName, TypeID, SupplierID, Price, Quantity, Total,
    #                                                  ReorderLevel, DateSupplied)
    #                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    #                            """, (name, type_id, supplier_id, price, quantity, total, reorder, date_supplied))
    #             self.conn.commit()
    #             cursor.close()
    #             QMessageBox.information(dialog, "Success", "Product added successfully.")
    #             dialog.accept()
    #             self.load_products()  # refresh table
    #         except Exception as e:
    #             QMessageBox.critical(dialog, "Database Error", f"Failed to insert product:\n{str(e)}")
    #
    #     add_btn.clicked.connect(save_product)
    #     dialog.exec()
    #
    #     # -----------------------------------------------------
    #     # UPDATE PRODUCT
    #     # -----------------------------------------------------
    #
    # def update_product(self):
    #     row = self.table.currentRow()
    #     if row == -1:
    #         QMessageBox.warning(self, "No product selected", "Select a product to update first.")
    #         return
    #
    #     # Fetch current product details
    #     product_id = self.table.item(row, 0).text()
    #     product_name = self.table.item(row, 1).text()
    #     product_type = self.table.item(row, 2).text()
    #     supplier_name = self.table.item(row, 3).text()
    #     price = self.table.item(row, 4).text()
    #     quantity = self.table.item(row, 5).text()
    #     total = self.table.item(row, 6).text()
    #     reorder = self.table.item(row, 7).text()
    #     date_supplied = self.table.item(row, 8).text()  # fetch current DateSupplied
    #
    #     dialog = QDialog(self)
    #     dialog.setWindowTitle(f"Update Product ID: {product_id}")
    #     dialog.setFixedSize(400, 650)
    #     dialog.setStyleSheet("""
    #         QDialog { background-color: rgb(70,70,70); border-radius: 10px; }
    #         QLabel { font-size: 14px; font-weight: bold; color: white; background-color: rgb(70, 70, 70) }
    #         QLineEdit { background-color: white; border: 1px solid rgb(120,120,120); border-radius: 10px; padding: 4px; font-size: 13px; color: black; }
    #         QComboBox { background-color: rgb(100,100,100); border: 1px solid rgb(120,120,120); border-radius: 10px; padding: 4px; font-size: 13px; color: black; }
    #         QComboBox QAbstractItemView { background-color: white; selection-background-color: rgb(70,130,250); selection-color: white; color: black; border-radius: 6px; }
    #         QPushButton { background-color: rgb(50,150,200); color: white; font-weight: bold; border-radius: 6px; padding: 6px; }
    #         QPushButton:hover { background-color: rgb(70,170,220); }
    #         QPushButton:pressed { background-color: rgb(30,130,180); }
    #         QLineEdit:disabled { background-color: rgb(200,200,200); color: #333; }
    #         QDateTimeEdit { background-color: white; border: 1px solid rgb(120,120,120); border-radius: 10px; padding: 4px; font-size: 13px; color: black; }
    #         QMessageBox {
    #             background-color: rgb(40,40,40);
    #             color: white;
    #             font-size: 14px;
    #         }
    #         QMessageBox QLabel {
    #             color: white;
    #         }
    #     """)
    #
    #     layout = QVBoxLayout(dialog)
    #     layout.setSpacing(10)
    #
    #     # === Input Fields ===
    #     id_label = QLabel("Product ID:")
    #     id_input = QLineEdit(product_id)
    #     id_input.setDisabled(True)
    #
    #     name_label = QLabel("Product Name:")
    #     name_input = QLineEdit(product_name)
    #
    #     price_label = QLabel("Price:")
    #     price_input = QLineEdit(price)
    #
    #     quantity_label = QLabel("Quantity:")
    #     quantity_input = QLineEdit(quantity)
    #
    #     total_label = QLabel("Total:")
    #     total_input = QLineEdit(total)
    #     total_input.setDisabled(True)
    #
    #     reorder_label = QLabel("Reorder Level:")
    #     reorder_input = QLineEdit(reorder)
    #
    #     type_label = QLabel("Type:")
    #     type_combo = QComboBox()
    #     # Load types from DB
    #     cursor = self.conn.cursor()
    #     cursor.execute("SELECT TypeID, TypeName FROM type")
    #     type_mapping = {}
    #     for tid, tname in cursor.fetchall():
    #         type_combo.addItem(tname, tid)
    #         type_mapping[tname] = tid
    #     cursor.close()
    #     if product_type in type_mapping:
    #         type_combo.setCurrentText(product_type)
    #
    #     supplier_label = QLabel("Supplier:")
    #     supplier_input = QLineEdit(supplier_name)
    #
    #     # --- NEW DateSupplied Field ---
    #     date_label = QLabel("Date Supplied:")
    #     date_input = QDateTimeEdit()
    #     date_input.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
    #     date_input.setCalendarPopup(True)
    #     # Prefill current DateSupplied
    #     date_input.setDateTime(QDateTime.fromString(date_supplied, "yyyy-MM-dd HH:mm:ss"))
    #
    #     # === Auto-calculate total when price or quantity changes ===
    #     def calculate_total():
    #         try:
    #             p = float(price_input.text()) if price_input.text() else 0
    #             q = int(quantity_input.text()) if quantity_input.text() else 0
    #             total_input.setText(f"{p * q:.2f}")
    #         except ValueError:
    #             total_input.setText("")
    #
    #     price_input.textChanged.connect(calculate_total)
    #     quantity_input.textChanged.connect(calculate_total)
    #
    #     # === Buttons ===
    #     btn_layout = QHBoxLayout()
    #     save_btn = QPushButton("Update Product")
    #     cancel_btn = QPushButton("Cancel")
    #     btn_layout.addWidget(save_btn)
    #     btn_layout.addWidget(cancel_btn)
    #     cancel_btn.clicked.connect(dialog.reject)
    #
    #     # === Add Widgets to Layout ===
    #     layout.addWidget(id_label)
    #     layout.addWidget(id_input)
    #     layout.addWidget(name_label)
    #     layout.addWidget(name_input)
    #     layout.addWidget(price_label)
    #     layout.addWidget(price_input)
    #     layout.addWidget(quantity_label)
    #     layout.addWidget(quantity_input)
    #     layout.addWidget(total_label)
    #     layout.addWidget(total_input)
    #     layout.addWidget(reorder_label)
    #     layout.addWidget(reorder_input)
    #     layout.addWidget(type_label)
    #     layout.addWidget(type_combo)
    #     layout.addWidget(supplier_label)
    #     layout.addWidget(supplier_input)
    #     layout.addWidget(date_label)
    #     layout.addWidget(date_input)
    #     layout.addLayout(btn_layout)
    #
    #     # === Save updated product to DB ===
    #     def save_update():
    #         name = name_input.text().strip()
    #         price_val = price_input.text().strip()
    #         quantity_val = quantity_input.text().strip()
    #         total_val = total_input.text().strip()
    #         reorder_val = reorder_input.text().strip()
    #         type_id = type_combo.currentData()
    #         supplier_name_val = supplier_input.text().strip()
    #         date_supplied_val = date_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")  # new date
    #
    #         if not supplier_name_val:
    #             QMessageBox.warning(dialog, "Input Error", "Supplier name is required.")
    #             return
    #
    #         # Check or insert supplier
    #         try:
    #             cursor = self.conn.cursor()
    #             cursor.execute("SELECT SupplierID FROM suppliers WHERE SupplierName=%s", (supplier_name_val,))
    #             result = cursor.fetchone()
    #             if result:
    #                 supplier_id = result[0]
    #             else:
    #                 cursor.execute("INSERT INTO suppliers (SupplierName) VALUES (%s)", (supplier_name_val,))
    #                 self.conn.commit()
    #                 supplier_id = cursor.lastrowid
    #             cursor.close()
    #         except Exception as e:
    #             QMessageBox.critical(dialog, "Database Error", f"Failed to check/insert supplier:\n{str(e)}")
    #             return
    #
    #         # Validation
    #         if not all([name, price_val, quantity_val, reorder_val]):
    #             QMessageBox.warning(dialog, "Input Error", "All fields are required.")
    #             return
    #
    #         try:
    #             price_val = float(price_val)
    #             quantity_val = int(quantity_val)
    #             reorder_val = int(reorder_val)
    #             total_val = price_val * quantity_val
    #         except ValueError:
    #             QMessageBox.warning(dialog, "Input Error", "Price, Quantity, and Reorder Level must be numeric.")
    #             return
    #
    #         # Confirmation
    #         confirm = QMessageBox.question(
    #             dialog,
    #             "Confirm Update",
    #             f"Update product {product_id} with new details?\n\n"
    #             f"Name: {name}\nPrice: {price_val}\nQuantity: {quantity_val}\n"
    #             f"Total: {total_val}\nReorder Level: {reorder_val}\nDate Supplied: {date_supplied_val}",
    #             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    #         )
    #
    #         if confirm != QMessageBox.StandardButton.Yes:
    #             return
    #
    #         # Update DB
    #         try:
    #             cursor = self.conn.cursor()
    #             cursor.execute("""
    #                            UPDATE products
    #                            SET ProductName=%s,
    #                                TypeID=%s,
    #                                SupplierID=%s,
    #                                Price=%s,
    #                                Quantity=%s,
    #                                Total=%s,
    #                                ReorderLevel=%s,
    #                                DateSupplied=%s
    #                            WHERE ProductID = %s
    #                            """, (name, type_id, supplier_id, price_val, quantity_val, total_val, reorder_val,
    #                                  date_supplied_val, product_id))
    #             self.conn.commit()
    #             cursor.close()
    #             QMessageBox.information(dialog, "Success", f"Product {product_id} updated successfully.")
    #             dialog.accept()
    #             self.load_products()
    #         except Exception as e:
    #             QMessageBox.critical(dialog, "Database Error", f"Failed to update product:\n{str(e)}")
    #
    #     save_btn.clicked.connect(save_update)
    #     dialog.exec()
    #
    #     # -----------------------------------------------------
    #     # DELETE PRODUCT
    #     # -----------------------------------------------------
    #
    # def delete_product(self):
    #     row = self.table.currentRow()
    #     if row == -1:
    #         QMessageBox.warning(self, "No product selected", "Select a product to delete.")
    #         return
    #
    #     product_id = self.table.item(row, 0).text()
    #
    #     # Confirm deletion
    #     confirm = QMessageBox.question(
    #         self,
    #         "Confirm Delete",
    #         f"Are you sure you want to permanently delete Product ID {product_id}?\n"
    #         "This will also delete all related stock-in and stock-out records.",
    #         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    #     )
    #
    #     if confirm != QMessageBox.StandardButton.Yes:
    #         return
    #
    #     try:
    #         cursor = self.conn.cursor()
    #
    #         # Delete related records in stockin and stockout first
    #         cursor.execute("DELETE FROM stockin WHERE ProductID = %s", (product_id,))
    #         cursor.execute("DELETE FROM stockout WHERE ProductID = %s", (product_id,))
    #
    #         # Now delete the product itself
    #         cursor.execute("DELETE FROM products WHERE ProductID = %s", (product_id,))
    #         self.conn.commit()
    #         cursor.close()
    #
    #         # Remove from table
    #         self.table.removeRow(row)
    #
    #         QMessageBox.information(
    #             self,
    #             "Deleted",
    #             f"Product ID {product_id} and its related stock-in/out records have been deleted successfully."
    #         )
    #
    #     except Exception as e:
    #         QMessageBox.critical(self, "Database Error", f"Failed to delete product:\n{str(e)}")

        # -----------------------------------------------------
        # STOCK IN
        # -----------------------------------------------------

    def stock_in(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Stock In Products")
        dialog.setFixedSize(700, 550)
        dialog.setStyleSheet("""
            QDialog { background-color: rgb(70,70,70); border-radius: 10px; }
            QLabel { font-size: 14px; color: white; font-weight: bold; }
            QLineEdit { color: black; background-color: white; border-radius: 6px; padding: 4px; font-size: 13px; }
            QPushButton { background-color: rgb(50,150,200); color: white; font-weight: bold; border-radius: 6px; padding: 6px; }
            QPushButton:hover { background-color: rgb(70,170,220); }
            QPushButton:pressed { background-color: rgb(30,130,180); }
            QTableWidget {
                    color: black;
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
                QHeaderView::section:first {
                    border-top-left-radius: 10px;
                }

                /* Rightmost header cell */
                QHeaderView::section:last {
                    border-top-right-radius: 10px;
                }

                QTableCornerButton::section {
                    background-color: rgb(50,150,200);
                    border: none;
                }

                /* ===== Vertical Scrollbar ===== */
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
                QMessageBox {
                    background-color: rgb(40,40,40);
                    color: white;
                    font-size: 14px;
                }
                QMessageBox QLabel {
                    color: white;
                }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)

        # === Top Panel: Product Details ===
        top_panel = QWidget()
        top_layout = QGridLayout(top_panel)
        top_layout.setSpacing(10)

        labels = ["ProductID", "Type", "ProductName", "Supplier", "Price", "Quantity", "Total", "Reorder Level",
                  "Date Supplied"]
        fields = {}
        for i, label_text in enumerate(labels):
            lbl = QLabel(f"{label_text}:")
            field = QLineEdit()
            field.setReadOnly(True)
            field.setStyleSheet("background-color: rgb(200,200,200); color: #333; border-radius: 6px;")
            row = i // 2
            col = (i % 2) * 2
            top_layout.addWidget(lbl, row, col)
            top_layout.addWidget(field, row, col + 1)
            fields[label_text] = field

        # Quantity to stock in input
        qty_label = QLabel("Quantity Stocked In:")
        qty_input = QLineEdit()
        qty_input.setPlaceholderText("Enter quantity received")
        top_layout.addWidget(qty_label, 5, 0)
        top_layout.addWidget(qty_input, 5, 1)

        layout.addWidget(top_panel)

        # === Product Table ===
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(
            ["ProductID", "ProductName", "Type", "Supplier", "Quantity", "Price", "Reorder Level"])
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.setFixedHeight(250)
        table.verticalHeader().setVisible(False)
        layout.addWidget(table)

        # Load products
        cursor = self.conn.cursor()
        cursor.execute("""
                       SELECT p.ProductID,
                              p.ProductName,
                              t.TypeName,
                              s.SupplierName,
                              p.Quantity,
                              p.Price,
                              p.ReorderLevel
                       FROM products AS p
                                LEFT JOIN type AS t ON p.TypeID = t.TypeID
                                LEFT JOIN suppliers AS s ON p.SupplierID = s.SupplierID
                       """)
        rows = cursor.fetchall()
        cursor.close()

        table.setRowCount(0)
        for row_data in rows:
            row = table.rowCount()
            table.insertRow(row)
            for col, data in enumerate(row_data):
                table.setItem(row, col, QTableWidgetItem(str(data)))

        # === Table selection updates top panel ===
        def update_top_panel():
            row = table.currentRow()
            if row == -1:
                for f in fields.values():
                    f.clear()
                return
            for i, key in enumerate(
                    ["ProductID", "ProductName", "Type", "Supplier", "Quantity", "Price", "Reorder Level"]):
                fields[key].setText(table.item(row, i).text())

            # Fetch DateSupplied from DB
            product_id = table.item(row, 0).text()
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DateSupplied, Quantity*Price FROM products WHERE ProductID=%s", (product_id,))
                result = cursor.fetchone()
                cursor.close()
                if result:
                    date_supplied, total = result
                    fields["Date Supplied"].setText(str(date_supplied))
                    fields["Total"].setText(f"{total:.2f}")
            except Exception as e:
                QMessageBox.critical(dialog, "Database Error", str(e))

        table.itemSelectionChanged.connect(update_top_panel)

        # === Confirm Stock In ===
        def confirm_stock_in():
            row = table.currentRow()
            if row == -1:
                QMessageBox.warning(dialog, "Warning", "Select a product from the table first.")
                return

            qty_received = qty_input.text().strip()
            if not qty_received:
                QMessageBox.warning(dialog, "Input Error", "Enter quantity to stock in.")
                return
            try:
                qty_received = int(qty_received)
                if qty_received <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(dialog, "Input Error", "Quantity must be a positive integer.")
                return

            product_id = table.item(row, 0).text()
            current_qty = int(fields["Quantity"].text())
            new_qty = current_qty + qty_received
            new_total = float(fields["Price"].text()) * new_qty
            new_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                # --- Update products table ---
                cursor = self.conn.cursor()
                cursor.execute("""
                               UPDATE products
                               SET Quantity=%s,
                                   Total=%s,
                                   DateSupplied=%s
                               WHERE ProductID = %s
                               """, (new_qty, new_total, new_date, product_id))

                # --- Insert into stockin table ---
                cursor.execute("""
                               INSERT INTO stockin (ProductID, AccountID, Quantity)
                               VALUES (%s, %s, %s)
                               """, (product_id, self.current_user_id, qty_received))  # <-- Use your logged-in staff's AccountID

                self.conn.commit()
                cursor.close()

                # Success message
                msg = QMessageBox(dialog)
                msg.setWindowTitle("Success")
                msg.setText(f"Stock updated for ProductID {product_id}!\nNew quantity: {new_qty}")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setStyleSheet("""
                                    QMessageBox { background-color: white; color: black; font-size: 14px; font-weight: bold; }
                                    QPushButton { background-color: rgb(50,150,200); color: white; border-radius: 6px; padding: 4px; font-weight: bold; }
                                    QPushButton:hover { background-color: rgb(70,170,220); }
                                    QPushButton:pressed { background-color: rgb(30,130,180); }
                                """)
                msg.exec()

                dialog.accept()
                self.load_products()
            except Exception as e:
                QMessageBox.critical(dialog, "Database Error", str(e))

        # === Buttons ===
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Confirm Stock In")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        cancel_btn.clicked.connect(dialog.reject)
        save_btn.clicked.connect(confirm_stock_in)
        layout.addLayout(btn_layout)

        dialog.exec()

        # -----------------------------------------------------
        # STOCK OUT
        # -----------------------------------------------------

    def stock_out(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Stock Out Products")
        dialog.setFixedSize(700, 550)
        dialog.setStyleSheet("""
            QDialog { background-color: rgb(70,70,70); border-radius: 10px; }
            QLabel { font-size: 14px; color: white; font-weight: bold; }
            QLineEdit { color: black; background-color: white; border-radius: 6px; padding: 4px; font-size: 13px; }
            QPushButton { background-color: rgb(50,150,200); color: white; font-weight: bold; border-radius: 6px; padding: 6px; }
            QPushButton:hover { background-color: rgb(70,170,220); }
            QPushButton:pressed { background-color: rgb(30,130,180); }
            QTableWidget {
                    color: black;
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
                QHeaderView::section:first {
                    border-top-left-radius: 10px;
                }

                /* Rightmost header cell */
                QHeaderView::section:last {
                    border-top-right-radius: 10px;
                }

                QTableCornerButton::section {
                    background-color: rgb(50,150,200);
                    border: none;
                }

                /* ===== Vertical Scrollbar ===== */
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
                QMessageBox {
                    background-color: rgb(40,40,40);
                    color: white;
                    font-size: 14px;
                }
                QMessageBox QLabel {
                    color: white;
                }
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(10)

        # === Top Panel: Product Details ===
        top_panel = QWidget()
        top_layout = QGridLayout(top_panel)
        top_layout.setSpacing(10)

        labels = ["ProductID", "Type", "ProductName", "Supplier", "Price", "Quantity", "Total", "Reorder Level",
                  "Date Supplied"]
        fields = {}
        for i, label_text in enumerate(labels):
            lbl = QLabel(f"{label_text}:")
            field = QLineEdit()
            field.setReadOnly(True)
            field.setStyleSheet("background-color: rgb(200,200,200); color: #333; border-radius: 6px;")
            row = i // 2
            col = (i % 2) * 2
            top_layout.addWidget(lbl, row, col)
            top_layout.addWidget(field, row, col + 1)
            fields[label_text] = field

        qty_label = QLabel("Quantity Issued:")
        qty_input = QLineEdit()
        qty_input.setPlaceholderText("Enter quantity to issue")
        top_layout.addWidget(qty_label, 5, 0)
        top_layout.addWidget(qty_input, 5, 1)
        layout.addWidget(top_panel)

        # === Product Table ===
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels(
            ["ProductID", "ProductName", "Type", "Supplier", "Quantity", "Price", "Reorder Level"]
        )
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.setFixedHeight(250)
        table.verticalHeader().setVisible(False)
        layout.addWidget(table)

        # === Load products ===
        cursor = self.conn.cursor()
        cursor.execute("""
                       SELECT p.ProductID,
                              p.ProductName,
                              t.TypeName,
                              s.SupplierName,
                              p.Quantity,
                              p.Price,
                              p.ReorderLevel
                       FROM products AS p
                                LEFT JOIN type AS t ON p.TypeID = t.TypeID
                                LEFT JOIN suppliers AS s ON p.SupplierID = s.SupplierID
                       """)
        rows = cursor.fetchall()
        cursor.close()

        table.setRowCount(0)
        for row_data in rows:
            row = table.rowCount()
            table.insertRow(row)
            for col, data in enumerate(row_data):
                table.setItem(row, col, QTableWidgetItem(str(data)))

        # === Update top panel on selection ===
        def update_top_panel():
            row = table.currentRow()
            if row == -1:
                for f in fields.values():
                    f.clear()
                return

            for i, key in enumerate(
                    ["ProductID", "ProductName", "Type", "Supplier", "Quantity", "Price", "Reorder Level"]):
                fields[key].setText(table.item(row, i).text())

            product_id = table.item(row, 0).text()
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT DateSupplied, Quantity*Price FROM products WHERE ProductID=%s", (product_id,))
                result = cursor.fetchone()
                cursor.close()
                if result:
                    date_supplied, total = result
                    fields["Date Supplied"].setText(str(date_supplied))
                    fields["Total"].setText(f"{total:.2f}")
            except Exception as e:
                QMessageBox.critical(dialog, "Database Error", str(e))

        table.itemSelectionChanged.connect(update_top_panel)

        # === Confirm Stock Out ===
        def confirm_stock_out():
            row = table.currentRow()
            if row == -1:
                QMessageBox.warning(dialog, "Warning", "Select a product from the table first.")
                return

            qty_issued = qty_input.text().strip()
            if not qty_issued:
                QMessageBox.warning(dialog, "Input Error", "Enter quantity to issue.")
                return
            try:
                qty_issued = int(qty_issued)
                if qty_issued <= 0:
                    raise ValueError
            except ValueError:
                QMessageBox.warning(dialog, "Input Error", "Quantity must be a positive integer.")
                return

            product_id = table.item(row, 0).text()
            current_qty = int(fields["Quantity"].text())

            if qty_issued > current_qty:
                QMessageBox.warning(dialog, "Input Error", "Cannot issue more than current stock.")
                return

            new_qty = current_qty - qty_issued
            new_total = float(fields["Price"].text()) * new_qty
            date_issued = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                cursor = self.conn.cursor()

                # Update products
                cursor.execute("""
                    UPDATE products
                    SET Quantity=%s,
                        Total=%s,
                        DateSupplied=%s
                    WHERE ProductID = %s
                """, (new_qty, new_total, date_issued, product_id))

                # Get the current user’s AccountID
                cursor.execute("SELECT AccountID FROM accounts WHERE Username = %s", (self.username,))
                account = cursor.fetchone()
                if account:
                    account_id = account[0]

                    cursor.execute("""
                        INSERT INTO stockout (ProductID, AccountID, Quantity)
                        VALUES (%s, %s, %s)
                    """, (product_id, account_id, qty_issued))
                else:
                    QMessageBox.warning(dialog, "Warning", "Unable to find current user account.")
                    cursor.close()
                    return

                self.conn.commit()
                cursor.close()

                # Success message
                msg = QMessageBox(dialog)
                msg.setWindowTitle("Success")
                msg.setText(f"Stock issued for ProductID {product_id}!\nNew quantity: {new_qty}")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setStyleSheet("""
                    QMessageBox { background-color: white; color: black; font-size: 14px; font-weight: bold; }
                    QPushButton { background-color: rgb(50,150,200); color: white; border-radius: 6px; padding: 4px; font-weight: bold; }
                    QPushButton:hover { background-color: rgb(70,170,220); }
                    QPushButton:pressed { background-color: rgb(30,130,180); }
                """)
                msg.exec()

                dialog.accept()
                self.load_products()

            except Exception as e:
                QMessageBox.critical(dialog, "Database Error", str(e))

        # === Buttons ===
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Confirm Stock Out")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        cancel_btn.clicked.connect(dialog.reject)
        save_btn.clicked.connect(confirm_stock_out)
        layout.addLayout(btn_layout)

        dialog.exec()

    def show_category_panel(self):
        self.hide_all_panels()

        if not hasattr(self, 'category_panel') or self.category_panel is None:
            self.category_panel = QWidget(self.analyticPanel)
            self.category_panel.setGeometry(10, 10, 1140, 500)
            self.category_panel.setStyleSheet("background-color: rgb(100, 100, 100); border-radius: 10px;")

            # Header label
            label = QLabel("Category Tables", self.category_panel)
            label.setGeometry(20, 10, 400, 40)
            label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")

            # === Common table style ===
            table_style = """
                QTableWidget {
                    color: black;
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
                QHeaderView::section:first {
                    border-top-left-radius: 10px;
                }

                /* Rightmost header cell */
                QHeaderView::section:last {
                    border-top-right-radius: 10px;
                }

                QTableCornerButton::section {
                    background-color: rgb(50,150,200);
                    border: none;
                }

                /* ===== Vertical Scrollbar ===== */
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

                /* ===== Horizontal Scrollbar (bottom) ===== */
                QScrollBar:horizontal {
                    background: #e2e2e2;
                    height: 10px;
                    margin: 0 2px 0 2px;
                    border-radius: 5px;
                }
                QScrollBar::handle:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb(130,180,230), stop:1 rgb(90,150,210));
                    border-radius: 20px;
                    min-width: 20px;
                }
                QScrollBar::handle:horizontal:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb(150,200,250), stop:1 rgb(100,160,220));
                }
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    width: 0px;
                    background: none;
                }
                QMessageBox {
                    background-color: rgb(40,40,40);
                    color: white;
                    font-size: 14px;
                }
                QMessageBox QLabel {
                    color: white;
                }
            """

            # === Category Table ===
            self.category_table = QTableWidget(self.category_panel)
            self.category_table.setGeometry(20, 60, 300, 420)
            self.category_table.setColumnCount(2)
            self.category_table.setHorizontalHeaderLabels(["CategoryID", "CategoryName"])
            self.category_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.category_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.category_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.category_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.category_table.setStyleSheet(table_style)
            self.category_table.setAlternatingRowColors(True)
            self.category_table.verticalHeader().setVisible(False)

            # === Type Table ===
            self.type_table = QTableWidget(self.category_panel)
            self.type_table.setGeometry(340, 60, 300, 420)
            self.type_table.setColumnCount(2)
            self.type_table.setHorizontalHeaderLabels(["TypeID", "TypeName"])
            self.type_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.type_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.type_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.type_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.type_table.setStyleSheet(table_style)
            self.type_table.setAlternatingRowColors(True)
            self.type_table.verticalHeader().setVisible(False)

            # === Product Table ===
            self.product_table = QTableWidget(self.category_panel)
            self.product_table.setGeometry(660, 60, 460, 420)
            self.product_table.setColumnCount(5)
            self.product_table.setHorizontalHeaderLabels(
                ["ProductID", "ProductName", "Price", "Quantity", "ReorderLevel"])
            self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.product_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            self.product_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
            self.product_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.product_table.setStyleSheet(table_style)
            self.product_table.setAlternatingRowColors(True)
            self.product_table.verticalHeader().setVisible(False)

            # === Load categories from DB ===
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT CategoryID, CategoryName FROM category ORDER BY CategoryName")
                categories = cursor.fetchall()
                cursor.close()

                self.category_table.setRowCount(0)
                for row_data in categories:
                    row = self.category_table.rowCount()
                    self.category_table.insertRow(row)
                    for col, data in enumerate(row_data):
                        self.category_table.setItem(row, col, QTableWidgetItem(str(data)))
            except Exception as e:
                QMessageBox.critical(self, "Database Error", str(e))

            # === Category clicked → load types ===
            def category_selected():
                row = self.category_table.currentRow()
                if row == -1:
                    self.type_table.setRowCount(0)
                    self.product_table.setRowCount(0)
                    return
                category_id = self.category_table.item(row, 0).text()
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT TypeID, TypeName FROM type WHERE CategoryID=%s ORDER BY TypeName",
                                   (category_id,))
                    types = cursor.fetchall()
                    cursor.close()

                    self.type_table.setRowCount(0)
                    self.product_table.setRowCount(0)
                    for row_data in types:
                        row_idx = self.type_table.rowCount()
                        self.type_table.insertRow(row_idx)
                        for col, data in enumerate(row_data):
                            self.type_table.setItem(row_idx, col, QTableWidgetItem(str(data)))
                except Exception as e:
                    QMessageBox.critical(self, "Database Error", str(e))

            self.category_table.itemSelectionChanged.connect(category_selected)

            # === Type clicked → load products ===
            def type_selected():
                row = self.type_table.currentRow()
                if row == -1:
                    self.product_table.setRowCount(0)
                    return
                type_id = self.type_table.item(row, 0).text()
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                                   SELECT ProductID, ProductName, Price, Quantity, ReorderLevel
                                   FROM products
                                   WHERE TypeID = %s
                                   ORDER BY ProductName
                                   """, (type_id,))
                    products = cursor.fetchall()
                    cursor.close()

                    self.product_table.setRowCount(0)
                    for row_data in products:
                        row_idx = self.product_table.rowCount()
                        self.product_table.insertRow(row_idx)
                        for col, data in enumerate(row_data):
                            self.product_table.setItem(row_idx, col, QTableWidgetItem(str(data)))
                except Exception as e:
                    QMessageBox.critical(self, "Database Error", str(e))

            self.type_table.itemSelectionChanged.connect(type_selected)

        self.category_panel.show()

    # def show_history_panel(self):
    #     self.hide_all_panels()
    #
    #     if not hasattr(self, 'history_panel') or self.history_panel is None:
    #         self.history_panel = QWidget(self.analyticPanel)
    #         self.history_panel.setGeometry(10, 10, 1140, 500)
    #         self.history_panel.setStyleSheet("background-color: rgb(100, 100, 100); border-radius: 10px;")
    #
    #         # Header label
    #         header_label = QLabel("Transaction History", self.history_panel)
    #         header_label.setGeometry(20, 10, 400, 40)
    #         header_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
    #
    #         table_style = """
    #             QTableWidget {
    #                 color: black;
    #                 background-color: #f8f9fa;
    #                 alternate-background-color: #e9ecef;
    #                 gridline-color: #b0b0b0;
    #                 border-radius: 10px;
    #                 font-size: 13px;
    #                 selection-background-color: rgb(70,130,250);
    #                 selection-color: white;
    #             }
    #
    #             QHeaderView::section {
    #                 background-color: rgb(50,150,200);
    #                 color: white;
    #                 font-weight: bold;
    #                 border: none;
    #                 padding: 6px;
    #             }
    #             QHeaderView::section:first {
    #                 border-top-left-radius: 10px;
    #             }
    #
    #             /* Rightmost header cell */
    #             QHeaderView::section:last {
    #                 border-top-right-radius: 10px;
    #             }
    #
    #             QTableCornerButton::section {
    #                 background-color: rgb(50,150,200);
    #                 border: none;
    #             }
    #
    #             /* ===== Vertical Scrollbar ===== */
    #             QScrollBar:vertical {
    #                 background: #e2e2e2;
    #                 width: 10px;
    #                 margin: 2px 0 2px 0;
    #                 border-radius: 5px;
    #             }
    #             QScrollBar::handle:vertical {
    #                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
    #                     stop:0 rgb(130,180,230), stop:1 rgb(90,150,210));
    #                 border-radius: 20px;
    #                 min-height: 20px;
    #             }
    #             QScrollBar::handle:vertical:hover {
    #                 background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
    #                     stop:0 rgb(150,200,250), stop:1 rgb(100,160,220));
    #             }
    #             QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    #                 height: 0px;
    #                 background: none;
    #             }
    #
    #             /* ===== Horizontal Scrollbar (bottom) ===== */
    #             QScrollBar:horizontal {
    #                 background: #e2e2e2;
    #                 height: 10px;
    #                 margin: 0 2px 0 2px;
    #                 border-radius: 5px;
    #             }
    #             QScrollBar::handle:horizontal {
    #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    #                     stop:0 rgb(130,180,230), stop:1 rgb(90,150,210));
    #                 border-radius: 20px;
    #                 min-width: 20px;
    #             }
    #             QScrollBar::handle:horizontal:hover {
    #                 background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
    #                     stop:0 rgb(150,200,250), stop:1 rgb(100,160,220));
    #             }
    #             QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    #                 width: 0px;
    #                 background: none;
    #             }
    #             QMessageBox {
    #                 background-color: rgb(40,40,40);
    #                 color: white;
    #                 font-size: 14px;
    #             }
    #             QMessageBox QLabel {
    #                 color: white;
    #             }
    #         """
    #
    #         # Stock In label
    #         stockin_label = QLabel("Stock Ins", self.history_panel)
    #         stockin_label.setGeometry(20, 60, 200, 30)
    #         stockin_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
    #
    #         # Stock In table
    #         self.stockin_table = QTableWidget(self.history_panel)
    #         self.stockin_table.setGeometry(20, 100, 1100, 160)
    #         self.stockin_table.setColumnCount(8)
    #         self.stockin_table.setHorizontalHeaderLabels([
    #             "ID", "ProductID", "ProductName", "Supplier", "Price", "Quantity", "Total", "Stocked By"
    #         ])
    #         self.stockin_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    #         self.stockin_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    #         self.stockin_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    #         self.stockin_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    #         self.stockin_table.verticalHeader().setVisible(False)
    #         self.stockin_table.setStyleSheet(table_style)
    #
    #         # Stock Out label
    #         stockout_label = QLabel("Stock Outs", self.history_panel)
    #         stockout_label.setGeometry(20, 280, 200, 30)
    #         stockout_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
    #
    #         # Refresh Button beside Stock Out label
    #         refresh_btn = QPushButton("⟳ Refresh", self.history_panel)
    #         refresh_btn.setGeometry(950, 280, 170, 30)
    #         refresh_btn.setStyleSheet("""
    #             QPushButton {
    #                 background-color: rgb(50,150,200);
    #                 color: white;
    #                 font-size: 14px;
    #                 font-weight: bold;
    #                 border-radius: 6px;
    #                 padding: 4px;
    #             }
    #             QPushButton:hover { background-color: rgb(70,170,220); }
    #             QPushButton:pressed { background-color: rgb(30,130,180); }
    #         """)
    #
    #         # Stock Out table
    #         self.stockout_table = QTableWidget(self.history_panel)
    #         self.stockout_table.setGeometry(20, 320, 1100, 160)
    #         self.stockout_table.setColumnCount(8)
    #         self.stockout_table.setHorizontalHeaderLabels([
    #             "ID", "ProductID", "ProductName", "Supplier", "Price", "Quantity", "Total", "Stocked By"
    #         ])
    #         self.stockout_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    #         self.stockout_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    #         self.stockout_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
    #         self.stockout_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    #         self.stockout_table.verticalHeader().setVisible(False)
    #         self.stockout_table.setStyleSheet(table_style)
    #
    #         # === Function to Load Data (used by refresh button and on open) ===
    #         def load_history_data():
    #             try:
    #                 cursor = self.conn.cursor()
    #                 # --- Stock In ---
    #                 cursor.execute("""
    #                                SELECT s.StockInID,
    #                                       p.ProductID,
    #                                       p.ProductName,
    #                                       sup.SupplierName,
    #                                       p.Price,
    #                                       s.Quantity                    AS QuantityAdded,
    #                                       (p.Price * s.Quantity)        AS Total,
    #                                       CONCAT(a.FName, ' ', a.LName) AS StockedBy
    #                                FROM stockin s
    #                                         JOIN products p ON s.ProductID = p.ProductID
    #                                         JOIN suppliers sup ON p.SupplierID = sup.SupplierID
    #                                         JOIN accounts a ON s.AccountID = a.AccountID
    #                                ORDER BY s.StockInID DESC
    #                                """)
    #                 stockins = cursor.fetchall()
    #
    #                 self.stockin_table.setRowCount(0)
    #                 for row_data in stockins:
    #                     row_idx = self.stockin_table.rowCount()
    #                     self.stockin_table.insertRow(row_idx)
    #                     for col, data in enumerate(row_data):
    #                         self.stockin_table.setItem(row_idx, col, QTableWidgetItem(str(data)))
    #
    #                 # --- Stock Out ---
    #                 cursor.execute("""
    #                                SELECT s.StockOutID,
    #                                       p.ProductID,
    #                                       p.ProductName,
    #                                       sup.SupplierName,
    #                                       p.Price,
    #                                       s.Quantity                    AS QuantityIssued,
    #                                       (p.Price * s.Quantity)        AS Total,
    #                                       CONCAT(a.FName, ' ', a.LName) AS StockedBy
    #                                FROM stockout s
    #                                         JOIN products p ON s.ProductID = p.ProductID
    #                                         JOIN suppliers sup ON p.SupplierID = sup.SupplierID
    #                                         JOIN accounts a ON s.AccountID = a.AccountID
    #                                ORDER BY s.StockOutID DESC
    #                                """)
    #                 stockouts = cursor.fetchall()
    #                 cursor.close()
    #
    #                 self.stockout_table.setRowCount(0)
    #                 for row_data in stockouts:
    #                     row_idx = self.stockout_table.rowCount()
    #                     self.stockout_table.insertRow(row_idx)
    #                     for col, data in enumerate(row_data):
    #                         self.stockout_table.setItem(row_idx, col, QTableWidgetItem(str(data)))
    #
    #             except Exception as e:
    #                 QMessageBox.critical(self, "Database Error", str(e))
    #
    #         # Connect the refresh button
    #         refresh_btn.clicked.connect(load_history_data)
    #
    #         # Initial load
    #         load_history_data()
    #
    #     self.history_panel.show()

    def show_account_panel(self):
        self.hide_all_panels()
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT username, fname, lname, role FROM accounts WHERE username=%s",
                (self.username,)
            )
            result = cursor.fetchone()
            cursor.close()

            if result:
                uname, fname, lname, role = result

                self.account_panel = QWidget(self.analyticPanel)
                self.account_panel.setGeometry(10, 10, 1140, 500)
                self.account_panel.setStyleSheet("background-color: rgb(100, 100, 100); border-radius: 10px;")

                account_title = QLabel("Account Details", self.account_panel)
                account_title.setGeometry(20, 10, 300, 40)
                account_title.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
                uname_label = QLabel(f"Username: {uname}", self.account_panel)
                fname_label = QLabel(f"Full name: {fname}", self.account_panel)
                lname_label = QLabel(f"Last Name: {lname}", self.account_panel)
                role_label = QLabel(f"Role: {role}", self.account_panel)

                uname_label.setGeometry(20, 70, 300, 40)
                fname_label.setGeometry(20, 120, 300, 40)
                lname_label.setGeometry(20, 170, 300, 40)
                role_label.setGeometry(20, 220, 300, 40)

                uname_label.setStyleSheet("color: white; font-size: 18px;")
                fname_label.setStyleSheet("color: white; font-size: 18px;")
                lname_label.setStyleSheet("color: white; font-size: 18px;")
                role_label.setStyleSheet("color: white; font-size: 18px;")

                self.account_panel.show()
            else:
                QMessageBox.information(self, "Account Details", "Account details not found.")

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    # ==========================
    # Logout Handler
    # ==========================
    def handle_back_btn_click(self, event):
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Logout")
        msg.setText("Are you sure you want to log out?\nYou will be returned to the login screen.")
        msg.setIcon(QMessageBox.Icon.Question)

        logout_btn = msg.addButton("Logout", QMessageBox.ButtonRole.YesRole)
        cancel_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.NoRole)
        msg.setDefaultButton(cancel_btn)
        msg.exec()

        if msg.clickedButton() == logout_btn:
            self.close()
            self.login_widget.setVisible(True)
