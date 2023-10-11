import csv
import re
import phonenumbers
import pandas as pd

# GUI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QColor

# Validations
name_regex = re.compile(r'^[A-Za-z\s]+$')
birthday_regex = re.compile(r'^(0[1-9]|1[0-2])/(0[1-9]|1[0-9]|2[0-9]|3[01])/(\d{2})$')
email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
phone_regex = re.compile(r'^\d{4}\s\d{3}\s\d{4}$')  

people = []
person = {}

# Read the data from the CSV file
with open('data.csv', 'r') as file:
    csv_reader = csv.reader(file)
    
    for row in csv_reader:
        if re.fullmatch(name_regex, row[0]):
            # If we're starting a new person and there's a previous person, append them to the people list
            if person:
                people.append(person)
            # Start a new person dictionary
            person = {"Name": row[0]}  
        elif re.fullmatch(birthday_regex, row[0]):
            person["Birthday"] = row[0]
        elif re.fullmatch(phone_regex, row[0]) and phonenumbers.is_valid_number(phonenumbers.parse(row[0], "PH")):
            person["Phone"] = row[0]
        elif re.fullmatch(email_regex, row[0]):
            person["Email"] = row[0]

    # Append the last person if they haven't been appended yet
    if person:
        people.append(person)

df = pd.DataFrame(people)

# Fill NaN values for Email, Phone, Birthday
df['Email'] = df['Email'].fillna('N/A')
df['Phone'] = df['Phone'].fillna('N/A')
df['Birthday'] = df['Birthday'].fillna('N/A')

# Create the main GUI window
class DataFrameViewer(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Joelflix Employees Database')
        self.setGeometry(500, 100, 850, 840)

        # Stylesheet
        stylesheet = """
            QHeaderView::section {
                background-color: #ffffff;
                color: black;
                padding: 6px;
                border: 0px solid #dcdcdc;
            }
        """
        self.setStyleSheet(stylesheet)

        # Create a standard item model
        self.model = QStandardItemModel(self.df.shape[0], self.df.shape[1])

        # Set column headers
        self.model.setHorizontalHeaderItem(0, QStandardItem())
        for col_idx, header in enumerate(self.df.columns):
            header_item = QStandardItem(header)
            header_item.setFont(QFont("Inter", 9, QFont.Bold))
            self.model.setHorizontalHeaderItem(col_idx + 1, header_item)

        # Populate the model with DataFrame values
        for row_idx in range(self.df.shape[0]):
            self.model.setItem(row_idx, 0, QStandardItem(str(row_idx + 1)))
            for col_idx in range(self.df.shape[1]):
                item = QStandardItem(str(self.df.iat[row_idx, col_idx]))
                if row_idx % 2 == 0:
                    item.setBackground(QColor('#F6F6F6'))
                elif row_idx % 2 == 1:
                    item.setBackground(QColor('#E6E6E6'))
                self.model.setItem(row_idx, col_idx + 1, item)

        # Create a tree view and set the model
        self.tree_view = QTreeView(self)
        self.tree_view.setModel(self.model)
        self.tree_view.resizeColumnToContents(0)
        self.tree_view.setColumnWidth(1, 200)

        # Create a search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.textChanged.connect(self.filter_data)

        # Create a layout for the search bar and tree view
        layout = QVBoxLayout()
        layout.addWidget(self.search_bar)
        layout.addWidget(self.tree_view)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def filter_data(self):
        search_text = self.search_bar.text().strip()
        if search_text:
            filtered_df = self.df[self.df.apply(lambda row: any(search_text in str(cell) for cell in row), axis=1)]
            self.update_model(filtered_df)
        else:
            self.update_model(self.df)

    def update_model(self, new_df):
        self.model.clear()
        self.model.setColumnCount(new_df.shape[1] + 1)
        self.model.setHorizontalHeaderItem(0, QStandardItem())
        for col_idx, header in enumerate(new_df.columns):
            header_item = QStandardItem(header)
            header_item.setFont(QFont("Inter", 9, QFont.Bold))
            self.model.setHorizontalHeaderItem(col_idx + 1, header_item)

        for row_idx in range(new_df.shape[0]):
            self.model.setItem(row_idx, 0, QStandardItem(str(row_idx + 1)))
            for col_idx in range(new_df.shape[1]):
                item = QStandardItem(str(new_df.iat[row_idx, col_idx]))
                if row_idx % 2 == 0:
                    item.setBackground(QColor('#F6F6F6'))
                elif row_idx % 2 == 1:
                    item.setBackground(QColor('#E6E6E6'))
                self.model.setItem(row_idx, col_idx + 1, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DataFrameViewer(df)
    viewer.show()
    sys.exit(app.exec_())
