import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

output_directory = 'C:\\your\\path'

csv_file_path = os.path.join(output_directory, 'crypto_data.csv')

driver = webdriver.Chrome()
url = 'https://finance.yahoo.com/crypto'
driver.get(url)

reject_button = driver.find_element(By.CLASS_NAME, 'btn.secondary.reject-all')
reject_button.click()

wait = WebDriverWait(driver, 10)
table = wait.until(EC.presence_of_element_located((By.ID, 'scr-res-table')))
time.sleep(3)

for _ in range(3):  # Scroll down 3x
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)  # load

table_rows = table.find_elements(By.TAG_NAME, 'tr')
data = []

for row in table_rows:
    columns = row.find_elements(By.TAG_NAME, 'td')
    row_data = [column.text.strip() for column in columns]
    data.append(row_data)

if os.path.exists(csv_file_path):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as existing_file:
        existing_reader = csv.reader(existing_file)
        header_row = next(existing_reader)
else:
    header_row = ['Symbol', 'Name', 'Price', 'Change', '% Change', 'Market Cap', 'Volume in Currency',
                  'Volume in Currency (24Hr)', 'Total Volume All Currencies (24Hr)', 'Circulating Supply']

open(csv_file_path, 'w').close()

# Write the header row back to the file
with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header_row)

# Append the new data
with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerows(data)

print("Data appended to 'crypto_data.csv'")
driver.quit()
