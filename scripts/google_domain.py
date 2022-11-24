#import selenium
import common_imports
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googleapiclient.discovery import build
from google.oauth2 import service_account
import gspread
import os
import json
from pathlib import Path
import time
import csv
from datetime import datetime
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# data extract function

def per_page_data(search_term):

    try:
        common_imports.comm_lib.scroll_page_end(driver,3)
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "result-list"))
        )
        domain_names = main.find_elements(By.CLASS_NAME,"row-disabled")
        i = 1

        for domain_name in domain_names:
            domain = domain_name.text
            web_scraper_start_url = driver.current_url
            web_scraper_order = i
            listdata = [web_scraper_order,web_scraper_start_url,domain]
            data.append(listdata)
            
            i +=1
        print(search_term," result count : ",len(domain_names)," ",datetime.now())
        return data


    except Exception as e:
        print(e)
        pass


# open the file in the append mode
def csvWriter(d):
    with open(f'C:\\Users\\shan cds\\Downloads\\google_domain_open_with{today}.csv','a',newline='',encoding='UTF8') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row header to the csv file
        writer.writerow(['web-scraper-order','web-scraper-start-url','domain'])
        # write a row data to the csv file
        writer.writerows(d)

def scrape(config,searchTerms):
    service_account_file = config["google_domain"]["googlesheet_auth"]["service_account_file"]
    spreadsheet_id = config["google_domain"]["googlesheet_auth"]["spreadsheet_id"]
    spreadsheet_name = config["google_domain"]["googlesheet_auth"]["spreadsheet_name"]
    try:
        input = driver.find_element(By.XPATH, '//*[@id="mat-input-0"]')
        input.clear()

        for i in searchTerms:
            input.send_keys(i)
            input.send_keys(Keys.RETURN)
            time.sleep(2)

            domain = per_page_data(i)
            time.sleep(5)
            input.clear()
            time.sleep(5)
    except :
        print('ERROR')
    print('count: ',len(domain))
    common_imports.comm_lib.googleSheetWrite(domain,service_account_file,spreadsheet_name,spreadsheet_id)

if __name__ == '__main__':
    today = str(datetime.today().strftime('%Y%m%d'))

    config_file = os.path.join(os.path.split(__file__)[0], Path(
    __file__).resolve().parents[1], 'config', 'config.json')
    f = open(config_file, encoding='utf-8')
    config = json.load(f)

    url = config["google_domain"]["url"]

    driver = uc.Chrome(use_subprocess=True)
    wait = WebDriverWait(driver,20)

    time.sleep(5)
    driver.get(url)

    time.sleep(10)



    driver.implicitly_wait(15)
    print(driver.title)


    searchTerms = config["search_terms"]["olympic"]

    data = [['web-scraper-order','web-scraper-start-url','domain']]
    search = driver.find_element(By.NAME,"domainsFindyBarInput")

    search.send_keys(searchTerms[0])
    search.send_keys(Keys.RETURN)

    # all_ending = driver.find_element(By.ID,"mat-tab-label-0-1")
    # time.sleep(2)
    # all_ending.click()
    time.sleep(5)
    driver.execute_script("document.body.style.zoom='90%'")
    time.sleep(2)
    driver.set_window_size(500, 950)

    try:
        driver.refresh()
        capture= driver.find_element(By.ID,"captcha-form")
        while capture.is_enabled():
            print("capture varification !")
            time.sleep(5)

    except:
        pass
    listdata = []
    scrape(config,searchTerms)


