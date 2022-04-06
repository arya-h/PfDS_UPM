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

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

START_DATE = '01/01/2020'
STOP_DATE = '12/31/2020'

assets = ['etfs/db-x-trackers-ii-global-sovereign-5', 'etfs/spdr-gold-trust', 'indices/usdollar',
          'etfs/ishares-global-corporate-bond-$', 'funds/amundi-msci-wrld-ae-c']


def scrape_data(start_date=START_DATE, stop_date=STOP_DATE, assets=assets):
    for asset in assets:
        driver = webdriver.Firefox()
        # XXX: is it cheating if we just go to the historical pages directly instead of clicking the button on the site?
        # 1. Go to historical data pages
        driver.get(f"https://www.investing.com/{asset}-historical-data")
        try:
            calender = driver.find_element(By.ID, 'widgetFieldDateRange')
            driver.execute_script("arguments[0].click();", calender)

            # 2. change start and stop date in calendar
            startDate = driver.find_element(By.ID, 'startDate')
            startDate.clear()
            startDate.send_keys(start_date)
            stopDate = driver.find_element(By.ID, 'endDate')
            stopDate.clear()
            stopDate.send_keys(stop_date)

            # 3. Click apply button
            apply_bttn = WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, "applyBtn")))
            driver.execute_script("arguments[0].click();", apply_bttn)
            time.sleep(2)

            # 4. TODO: Discard unused columns with headers Open, High and Low
            # TODO: handle missing dates
            table = driver.find_element(By.ID, 'curr_table')
            rows = table.find_elements(by=By.TAG_NAME, value='tr')
            df = pd.DataFrame([row.text.split(",") for row in rows])

            # 5. Download data
            df.to_csv(f'{asset.split(sep="/")[1]}.csv', header=True, index=False)
            print(f'Successfully stored {asset.split(sep="/")[1]}.csv')
        finally:
            driver.close()


scrape_data()
