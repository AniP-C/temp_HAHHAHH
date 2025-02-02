from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import openpyxl
from openpyxl import Workbook

# Dictionary with keys and multiple values
data = {
    "key1": ["G008020919", "1234421"],
    "key2": ["060062363"],
    
}

# Connect to an already opened Chrome session
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # Debugging port set in Chrome

driver = webdriver.Chrome(options=options)  # Connect to the existing session

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
    # Note: Do not quit the driver since it's connected to the live browser session
    pass

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
output_file = "search_results.xlsx"
wb.save(output_file)
print(f"Results saved to {output_file}")
