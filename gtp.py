from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import openpyxl
from openpyxl import Workbook

# Dictionary with keys and multiple values
data = {
    "key1": ["G008020919" , "1234421"],
    "key2": ["060062363"],
    # "key1":["1234421"]
}

# Prompt user for headless mode
# show_browser = input("Do you want to see browser operations? (yes/no): ").strip().lower()
show_browser = "no"
headless = show_browser != "yes"

# Set up Selenium with ChromeDriver
chrome_options = Options()
if headless:
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

service = Service("path/to/chromedriver")  # Replace with the path to your ChromeDriver
# driver = webdriver.Chrome(service=service, options=chrome_options)
driver = webdriver.Chrome()

# Initialize results list
results = []

try:
    for key, values in data.items():
        for value in values:
            url = f"https://direct.asda.com/george/clothing/10,default,sc.html?q={value}"  # Modify as needed
            driver.get(url)  # Open the URL

            try:
                # Check for the 'searchfail_text' class
                driver.find_element(By.CLASS_NAME, "searchfail_text")
                results.append((key, value, "Not present in website"))
            except NoSuchElementException:
                try:
                    # Check for the 'mini-container' class
                    driver.find_element(By.CLASS_NAME, "mini-container")
                    results.append((key, value, "Present in website"))
                except NoSuchElementException:
                    results.append((key, value, "Neither 'searchfail_text' nor 'mini-container' found"))
finally:
    driver.quit()

# Save results to an Excel file
wb = Workbook()
ws = wb.active
ws.title = "Search Results"

# Write header row
ws.append(["Key", "Value", "Status"])

# Write data rows
for key, value, status in results:
    ws.append([key, value, status])

# Save the Excel file
output_file = "search_results_1.xlsx"
wb.save(output_file)
print(f"Results saved to {output_file}")




"""

import pandas as pd

# Specify the column names
key_column = "Column1"
value_column = "Column2"

# Read the CSV file
df = pd.read_csv("your_file.csv")

# Create a dictionary from the two columns
result_dict = dict(zip(df[key_column], df[value_column]))

print(result_dict)


"""


"""
col1 col2
key1 val1
key1 val2
key2 val3
key3 val4
key1 val5
key2 val3
"""
