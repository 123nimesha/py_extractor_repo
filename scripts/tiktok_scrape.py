
import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException
from csv import DictWriter
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from googleapiclient.discovery import build
# import lib.lib as lib
from datetime import datetime
# from webdriver_manager.chrome import ChromeDriverManager
import pickle
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import os
from pathlib import Path
import json
import common_imports
import json
import os.path
from os import path


def saveCookies(config):
    if __name__ == '__main__':
        email = config["tiktok"]["user_name"]
        password = config["tiktok"]["password"]
        option = uc.ChromeOptions()
        option.add_argument('--disable-notifications')
        #options.add_argument('proxy-server=106.122.8.54:3128')
        #options.add_argument(r'--user-data-dir=C:\Users\suppo\AppData\Local\Google\Chrome\User Data\Default')

        driver = uc.Chrome(use_subprocess= True, options=option, headless=True)
        driver.get('https://www.tiktok.com/login/phone-or-email/email')

        driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email or username"]').send_keys(email)

        driver.find_element(
            By.CSS_SELECTOR, 'input[placeholder="Password"]').send_keys(password)

        driver.find_element(
            By.CSS_SELECTOR, 'button[data-e2e="login-button"]').click()

        time.sleep(10)

        cookies = driver.get_cookies()
        pickle.dump(cookies, open("scripts/tiktok_cookies.pkl", "wb"))

        driver.quit()


option = uc.ChromeOptions()
def loadCookies():
    if __name__ == '__main__':
        
        chrome_prefs = {}
        option.add_argument("--lang=en")
        option.add_argument("--disable-notifications")
        # chrome_prefs["profile.default_content_settings"] = {"images": 2}
        # chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        chrome_prefs["translate_whitelists"] = {"fr":"en","zh-CN":"en","zh-TW":"en","de":"en","ar":"en"}
        chrome_prefs["translate"] = {"enabled":"true"}
        option.experimental_options["prefs"] = chrome_prefs
        driver = uc.Chrome(use_subprocess= True, headless=False)
        driver.get(
            'https://www.tiktok.com/login/phone-or-email/email')
        
        try:
            cookies = pickle.load(open("scripts/tiktok_cookies.pkl", "rb"))
            for cookie in cookies:
                cookie['domain'] = ".tiktok.com"
                driver.add_cookie(cookie)
            
        except:
            pass
        return driver
        

def append_dict_as_row(file_name, dict_of_elem, field_names):
    # Open file in append mode
    with open(file_name, 'a+', newline='',encoding='utf-8') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict_of_elem)

def scroll():
    account_tab = driver.find_element(By.ID,'tabs-0-tab-search_account')
    account_tab.click()
    end_scroll = True
    lenOfPage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    driver.execute_script(f"window.scrollTo(0, {lenOfPage});")
    scrRan = 0
    while end_scroll:
        lastCount = lenOfPage
        for y in range(scrRan, int(lastCount), 10):
            driver.execute_script(f"window.scrollTo(0, {y});")
            scrRan = lastCount
        try:
            load_more = driver.find_element(By.CSS_SELECTOR,'button[data-e2e="search-load-more"]')
            load_more.click()
            time.sleep(4)
        except:
            pass
        lenOfPage = driver.execute_script("var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            for y in range(int(lastCount),0, -20):
                driver.execute_script(f"window.scrollTo(0, {y});")
            for y in range(0,int(lastCount), 20):
                driver.execute_script(f"window.scrollTo(0, {y});")
            break
        else:
            continue

def scrape(driver,url,search_terms,db,cursor,client):
    driver.get(url)
    time.sleep(5)
    for search_url in search_terms:
        # captcha_verify_container
        tiktok_accounts =[]
        insert_query = """INSERT IGNORE INTO `tiktok_users`
                        (`id`,
                        `profile_name`,
                        `url`,
                        `location`,
                        `search_term`,
                        `image`,
                        `description`,
                        `number_of_fans`,
                        `client`)
                        VALUES
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON DUPLICATE KEY
                            UPDATE `image`=%s;
                        """
        search_term = search_url.split("=")[1].split("&")[0]
        search_input = driver.find_element(By.TAG_NAME,'input')
        search_input.send_keys(str(search_term))
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)
        try:
            capture= driver.find_element(By.CLASS_NAME,"captcha_verify_container")
            while capture.is_enabled():
                print("capture varification !")
                time.sleep(5)
        except:
            pass
            time.sleep(4)
        
        scroll()
        search_users = driver.find_elements(By.CSS_SELECTOR, 'div[data-e2e="search-user-container"]')
        for ele in search_users:
            profile_url = ele.find_element(By.CSS_SELECTOR,'a[data-e2e="search-user-info-container"]').get_attribute('href')
            try:
                img = ele.find_element(By.TAG_NAME,'img').get_attribute('src')
            except:
                img=""
                pass
            decs = ele.text
            profile_name = ele.find_element(By.CSS_SELECTOR,'.tiktok-1bs6wz6-DivSubTitleWrapper').text
            
            try:
                location = ele.find_element(By.CSS_SELECTOR,'a._39g5').text
            except:
                location = None
                pass
            try:
                followers = ele.find_element(By.CSS_SELECTOR,'.tiktok-1bs6wz6-DivSubTitleWrapper strong, div.tiktok-1awssxn-DivLink:nth-of-type(n+2) div.tiktok-1bs6wz6-DivSubTitleWrapper span, p span').text
            except:
                followers = None
                pass
            # u_arr = {"profile_id":profile_url.split("?")[0].split("@")[1],
            # "profile_name":profile_name,
            # "url":profile_url,
            # "location":location,
            # "search_term":search_term,
            # "image":img,
            # "description":decs,
            # "number_of_fans":followers,
            # "client":client}
            # append_dict_as_row("daily_psg_tiktok_users.csv",u_arr,fileds_name)
            
            tiktok_accounts.append(
                (
                    profile_url.split("?")[0].split("@")[1],
                    profile_name.split("·")[0],
                    profile_url.split("?")[0],
                    location,
                    search_term,
                    img,
                    decs,
                    followers,
                    client,
                    img
                )
            )
        print(search_term ," search term result count :",len(tiktok_accounts)," ",datetime.now())
        #insert database
        try:
            cursor.executemany(insert_query, tiktok_accounts)
            db.commit()
            print('Added', cursor.rowcount, 'listings')
        except Exception as e:
            if(e.errno != 1062):
                insert_db_err = 'Database insert Error: ' + str(e)
                print(insert_db_err)
            pass
        search_input.clear()
    


if __name__ == '__main__':
    logo = "https://s3.amazonaws.com/cdn.legalbaseportal.com/tik-tok.png"
    config_file = os.path.join(os.path.split(__file__)[0], Path(
    __file__).resolve().parents[1], 'config', 'config.json')
    f = open(config_file, encoding='utf-8')
    config = json.load(f)
    search_terms = config["tiktok"]["search_url"]
    url = config["tiktok"]["base_url"]
    fileds_name =["profile_id","profile_name","url","location","search_term","image","description","number_of_fans","client"]
    u_arr = {"profile_id":"profile_id","profile_name":"profile_name","url":"url","location":"location","search_term":"search_term","image":"image","description":"description","number_of_fans":"number_of_fans","client":"client"}
    data_arr = []
    connection = common_imports.db_config.db_connection()
    db = connection["db"]
    cursor = connection["cursor"]
    clients = ["psg"]
    #append_dict_as_row("daily_psg_tiktok_users.csv",u_arr,fileds_name)
    # saveCookies(config)
    if path.exists('scripts/tiktok_cookies.pkl'):
        driver = loadCookies()
    else:
        saveCookies(config)
        driver = loadCookies()
    for client in clients:
        # common_imports.slack.send_notification(common_imports.slack.get_url(), 'Tiktok_users',
        #                                         ':large_blue_circle: ' + client.upper() + ' Started', logo)
        scrape(driver,url,search_terms,db,cursor,client)
    
    # common_imports.slack.send_notification(common_imports.slack.get_url(), 'Tiktok_users',
    #                                        ':white_check_mark: Complete', logo)