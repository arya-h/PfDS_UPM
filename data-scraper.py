### Firefox usage only
# Download geckodriver and ensure it can be found on your system path!

# Interest range: 01/01/2020 and 12/31/2020, inclusive, from investing.com
# Stored in individual .csv files:
#   amundi-msci-wrld-ae-c.csv
#   db-x-trackers-ii-global-sovereign-5.csv
#   ishares-global-corporate-bond-$.csv
#   spdr-gold-trust.csv
#   usdollar.csv
import time
import os

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium.common.exceptions import TimeoutException

START_DATE = '01/01/2020'
STOP_DATE = '12/31/2020'

assets = ['etfs/db-x-trackers-ii-global-sovereign-5', 'etfs/spdr-gold-trust', 'indices/usdollar',
          'etfs/ishares-global-corporate-bond-$', 'funds/amundi-msci-wrld-ae-c']


def scrape_data(start_date=START_DATE, stop_date=STOP_DATE, assets=assets):
    for asset in assets:
        driver = webdriver.Firefox()
        # 1. Go to historical data pages
        driver.get(f"https://www.investing.com/{asset}-historical-data")
        try:
            calender = driver.find_element(By.ID, 'widgetFieldDateRange')
            driver.execute_script("arguments[0].click();", calender)

            # 2. Change start and stop date in calendar
            # Wait until start and stop date field are loaded
            WebDriverWait(driver, 5).until(lambda d: d.find_element(by=By.ID, value="startDate"))
            startDate = driver.find_element(By.ID, 'startDate')
            startDate.clear()
            startDate.send_keys(start_date)
            stopDate = driver.find_element(By.ID, 'endDate')
            stopDate.clear()
            stopDate.send_keys(stop_date)

            # 3. Click apply button
            apply_btn = WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, "applyBtn")))
            driver.execute_script("arguments[0].click();", apply_btn)

            # Wait until old table is removed and new table is loaded to ensure correct data to be loaded
            WebDriverWait(driver, 2, ignored_exceptions=TimeoutException).until_not(
                lambda d: d.find_element(by=By.ID, value="curr_table"))
            table = WebDriverWait(driver, 5).until(lambda d: d.find_element(by=By.ID, value="curr_table"))

            thead = table.find_element(by=By.TAG_NAME, value='thead')
            header_rows = thead.find_element(by=By.TAG_NAME, value='tr')
            headers = header_rows.find_elements(by=By.TAG_NAME, value='th')
            header = []
            for h in headers:
                header.append(h.text)
            df = pd.DataFrame(columns=header)

            tbody = table.find_element(by=By.TAG_NAME, value='tbody')
            body_rows = tbody.find_elements(by=By.TAG_NAME, value='tr')
            for row in body_rows:
                cells = []
                current_cells = row.find_elements(by=By.TAG_NAME, value='td')
                for cell in current_cells:
                    cells.append(cell.text)
                length = len(df)
                df.loc[length] = cells

            # 4. Discard unused columns with headers Open, High and Low
            df = df.drop(['Open', 'High', 'Low'], axis=1)

            # Change Date column to proper format
            df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, "%b %d, %Y"))
            df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))

            # 5. Download data
            if not os.path.exists("data"):
                os.mkdir("data")
            df.to_csv(f'data/{asset.split(sep="/")[1]}.csv', header=True, index=False)
            print(f'Successfully stored {asset.split(sep="/")[1]}.csv in the data/ folder')
        finally:
            driver.close()


scrape_data()
