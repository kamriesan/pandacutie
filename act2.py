import csv
import re
import phonenumbers
import pandas as pd

# GUI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor  # Import QFont and QColor

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

# Fill NaN values for Email
df['Email'] = df['Email'].fillna('N/A')

# GUI 
class DataFrameViewer(QMainWindow):
    def __init__(self, df):
        super().__init__()
        self.df = df
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Joelflix Employees Database')
        self.setGeometry(500, 100, 850, 840)

        # Stylesheet for a formal blue appearance
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
        model = QStandardItemModel(self.df.shape[0], self.df.shape[1])  # Adjusted for the index column

        # Set column headers, including the index header
        model.setHorizontalHeaderItem(0, QStandardItem())
        for col_idx, header in enumerate(self.df.columns):
            header_item = QStandardItem(header)
            header_item.setFont(QFont("Inter", 9, QFont.Bold))  # Set font to Inter and bold
            model.setHorizontalHeaderItem(col_idx + 1, header_item)
        
        # Populate the model with DataFrame values
        for row_idx in range(self.df.shape[0]):
            model.setItem(row_idx, 0, QStandardItem(str(row_idx + 1)))  # Set the index starting from 1
            for col_idx in range(self.df.shape[1]):
                item = QStandardItem(str(self.df.iat[row_idx, col_idx]))
                # Set a background color for every other row
                if row_idx % 2 == 0:
                    item.setBackground(QColor('#F6F6F6'))  # darkey gray background
                elif row_idx % 2 == 1:
                    item.setBackground(QColor('#E6E6E6'))  # lighter gray background
                model.setItem(row_idx, col_idx + 1, item)

        # Create a tree view and set the model
        tree_view = QTreeView(self)
        tree_view.setModel(model)
        tree_view.resizeColumnToContents(0)  # Adjust the column index accordingly
        tree_view.setColumnWidth(1, 200)
        self.setCentralWidget(tree_view)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = DataFrameViewer(df)
    viewer.show()
    sys.exit(app.exec_())
