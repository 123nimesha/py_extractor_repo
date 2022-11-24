# import selenium

from datetime import datetime
import time
import gspread
import os
import json
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from googleapiclient.discovery import build
from google.oauth2 import service_account
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
import common_imports



def scrape(config,searchTerms):
    service_account_file = config["dnpedia_domain"]["googlesheet_auth"]["service_account_file"]
    spreadsheet_id = config["dnpedia_domain"]["googlesheet_auth"]["spreadsheet_id"]
    spreadsheet_name = config["dnpedia_domain"]["googlesheet_auth"]["spreadsheet_name"]
    if driver.find_element(By.XPATH, '//*[@id="dmsword"]').is_displayed():
        try:

            select_mode()
            for i in searchTerms:
                data = []
                type_key = driver.find_element(By.XPATH, '//*[@id="dmsword"]')
                type_key.send_keys(i, Keys.RETURN)
                while driver.find_element(By.ID,"load_domain-grid").is_displayed():
                    continue

                checkalt = alertCheck(driver)
                if checkalt == True:
                    while checkalt == True:
                        type_key.send_keys(Keys.RETURN)
                        time.sleep(10)
                        checkalt = alertCheck(driver)
                templist= getdata(i)
                type_key.clear()
            print('count: ', len(templist))
            common_imports.comm_lib.googleSheetWrite(templist,service_account_file,spreadsheet_name,spreadsheet_id)
            driver.close()
        except Exception as e:
            print(e)
            pass




# data extract function
def waitPageLoad():
    try:
        scroll_page_end()
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "domain-grid"))
        )



    except Exception as e:
        print(e)
        pass


# page scroll function until end of the page
def scroll_page_end():
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

    match = False
    while (match == False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            for y in range(0, int(lastCount), 10):
                driver.execute_script(f"window.scrollTo(0, {y});")
            print('page end...')
            match = True


def select_mode():
    mode = driver.find_element(By.XPATH, '//*[@id="searchmode"]/option[3]')
    mode.click()
    time.sleep(1)
    duration = driver.find_element(By.XPATH, '//*[@id="searchdays"]/option[2]')
    duration.click()
    time.sleep(1)
    itemCount = driver.find_element(By.XPATH,
                                    '//*[@id="domain-grid-pager_center"]/table/tbody/tr/td[8]/select/option[3]')
    itemCount.click()
    time.sleep(1)


def alertCheck(driver):
    driver = driver
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(20)
        print("alert accepted ")
        return True
    except Exception as e:
        print(e)
        pass
        return False
    time.sleep(5)

datalist = []
def getdata(search_term):
    r = 1
    table = driver.find_element(By.XPATH, '//*[@id="domain-grid"]/tbody').text
    datas = table.split('\n')

    for data in datas:
        row = data.split(' ')
        datalist.append(row)
        r += 1
    print(search_term, " results count :",len(datas)," ",datetime.now())
    return datalist



if __name__ == '__main__':
    today = datetime.today().strftime('%Y%m%d')

    config_file = os.path.join(os.path.split(__file__)[0], Path(
    __file__).resolve().parents[1], 'config', 'config.json')
    f = open(config_file, encoding='utf-8')
    config = json.load(f)

    try:
        # driver = uc.Chrome(use_subprocess=True)
        driver = uc.Chrome(use_subprocess=True,headless=False)

        url = config["dnpedia_domain"]["url"]
        driver.get(url)
        time.sleep(2)
        while driver.find_element(By.ID, "challenge-running").is_displayed():
            continue
    except Exception as e:
        print(e)
    print(driver.title)
    templist = []
    searchTerms = config["search_terms"]["olympic"]
    scrape(config,searchTerms)
    driver.quit()
    print('Done')