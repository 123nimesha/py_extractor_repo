import time
from selenium.webdriver.common.by import By
from google.oauth2 import service_account
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googleapiclient.discovery import build
from google.oauth2 import service_account
import gspread
import time
import csv
from datetime import datetime
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
today = str(datetime.today().strftime('%Y%m%d'))
import mysql.connector
from mysql.connector import errorcode




def sql_data_insert(data):

    try:
      cnx = mysql.connector.connect(user='root', password='0000',
                                  host='127.0.0.1',
                                  database='social_media_fb')
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
        try:
            mycursor = cnx.cursor()

            sql = "INSERT INTO social_media_fb.`11` (client, image, profile_name, url, profile_post, social_media_site, date_detected, number_of_fans, searh_terms, post_profile_url, description, post_profile_date) VALUES (%s, %s ,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
            val = data
            mycursor.execute(sql, val)

            cnx.commit()
        except mysql.connector.Error as e:
            print("Mysql Error :",e)

def scroll_page_end(driver,scroll_counter):
    driver = driver
    html = driver.find_element(By.TAG_NAME, 'html')
    
    time.sleep(5)
    for i in range(scroll_counter,0,-1):
        lenOfPage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        scrRan = 0
        while driver.find_element(By.TAG_NAME,'div'):
            lastCount = lenOfPage
            # for y in range(scrRan, int(lastCount), 10):
            #     driver.execute_script(f"window.scrollTo(0, {y});")
            html.send_keys(Keys.END)
            time.sleep(3)
            scrRan = lastCount
            lenOfPage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            

            # Divs = driver.find_element(By.TAG_NAME,'div')

            if lastCount == lenOfPage:
                for y in range(int(lastCount),0, -20):
                    driver.execute_script(f"window.scrollTo(0, {y});")
                for y in range(0,int(lastCount), 20):
                    driver.execute_script(f"window.scrollTo(0, {y});")
                break
            else:
                continue


def googleSheetWrite(list,SERVICE_ACCOUNT_FILE,SPREADSHEET_NAME,SPREADSHEET_ID):
    # Google Sheet API settings
    gsheet_is = True
    while gsheet_is:
        try:
            SERVICE_ACCOUNT_FILE = SERVICE_ACCOUNT_FILE
            SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
            creds = None
            creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            # The ID and range of a spreadsheet.
            #----------------------------------------------------------------
            SPREADSHEET_NAME = SPREADSHEET_NAME
            SPREADSHEET_ID = SPREADSHEET_ID
            #----------------------------------------------------------------

            service = build('sheets', 'v4', credentials=creds)
            sheet = service.spreadsheets()
            # add worksheet
            sa = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
            sh = sa.open(SPREADSHEET_NAME)
            sh.add_worksheet(today, 1000, 26, 0)
            time.sleep(5)
            # add values to the created work sheet
            request = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range=f'{today}!A:F',
                                                             valueInputOption='USER_ENTERED', body={'values': list})
            response = request.execute()

            print(response)
            gsheet_is = False
            
        except Exception as e:
            print('Error :',e)
            check = input('Check the Error..\n Do you want to upload the data again ? y/n\n')
            if check == 'n':
                gsheet_is = False
