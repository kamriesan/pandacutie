import pandas as pd

# Initialize empty lists to store data for each category
names = []
birthdays = []
phones = []
emails = []

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

# Create a DataFrame from the categorized data
data = {
    "Name": names,
    "Birthday": birthdays,
    "Phone": phones,
    "Email": emails
}
df = pd.DataFrame(data)

# Print the resulting DataFrame
print(df)
