import csv
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QFont, QColor  # Import QFont and QColor

# Read the data from the CSV file
names, birthdays, phones, emails = [], [], [], []
with open('data.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        if '@' in row[0]:
            current_category = "Email"
            emails.append(row[0])
        elif '/' in row[0]:
            current_category = "Birthday"
            birthdays.append(row[0])
        elif any(char.isdigit() for char in row[0]):
            current_category = "Phone"
            phones.append(row[0])
        else:
            current_category = "Name"
            names.append(row[0])

data = {
    "Name": names,
    "Birthday": birthdays,
    "Phone": phones,
    "Email": emails
}

df = pd.DataFrame(data)

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
