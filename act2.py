import tkinter as tk
from tkinter import ttk
import pandas as pd

# Initialize empty lists to store data for each category
names = []
birthdays = []
phones = []
emails = []

# Simulated data for demonstration
# Populate the lists from the simulated data
data = {
    "Name": names,
    "Birthday": birthdays,
    "Phone": phones,
    "Email": emails
}

# Read the data from the CSV file
with open('data.csv', 'r') as file:
    lines = file.readlines()
    current_category = None

    for line in lines:
        line = line.strip()
        
        # Check for the presence of specific characters to categorize data
        if '@' in line:
            current_category = "Email"
            emails.append(line)
        elif '/' in line:
            current_category = "Birthday"
            birthdays.append(line)
        elif any(char.isdigit() for char in line):
            current_category = "Phone"
            phones.append(line)
        else:
            current_category = "Name"
            names.append(line)

# Update the data dictionary with the populated lists
data = {
    "Name": names,
    "Birthday": birthdays,
    "Phone": phones,
    "Email": emails
}

df = pd.DataFrame(data)

# Create the main application window
root = tk.Tk()
root.title("Joelflix Employees Database")

# Create a treeview widget
tree = ttk.Treeview(root)

# Define columns
columns = ['Index'] + list(df.columns)  # Add an 'Index' column at the start
tree["columns"] = columns

# Configure column headings
for col in columns:
    tree.heading(col, text="" if col == "Index" else col, anchor="w")
    if col == "Index":
        tree.column(col, width=50)  # Set a smaller width for the 'Index' column

# Insert data into the treeview with an index starting from 1
for i, row in df.iterrows():
    values = [i + 1] + list(row.values)
    tree.insert("", "end", iid=i, values=values)

# Remove the blank column on the left
tree["show"] = "headings"

tree.pack(padx=20, pady=10, fill="both", expand=True)

root.mainloop()
