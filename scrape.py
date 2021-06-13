from  selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import os 
from dotenv import load_dotenv
import time



load_dotenv()





download_path="/home/pi/Desktop/ktu-result-notify/results"
option = webdriver.ChromeOptions()
option.headless = True
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')

option.add_experimental_option("prefs", {
    "download.default_directory" : download_path,
    'profile.default_content_setting_values.automatic_downloads': 2,
    "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
    })


def fetch_grade_card(username,password,sem):

    browser = webdriver.Chrome(options=option)

    browser.get('https://app.ktu.edu.in/login.jsp')


    username_elem = browser.find_element_by_name("username")
    password_elem = browser.find_element_by_name("password")

    username_elem.send_keys(username)
    password_elem.send_keys(password)

    browser.find_element_by_xpath('//*[@id="btn-login"]').click()

    result=browser.find_element_by_xpath('/html/body/div[3]/div[6]/div[1]/div/div/div[1]/ul/li[4]/a').click()

    select_dropdown=Select(browser.find_element_by_xpath('//*[@id="semesterGradeCardListingSearchForm_semesterId"]'))

    select_dropdown.select_by_visible_text(sem)

    search_button=browser.find_element_by_xpath('//*[@id="semesterGradeCardListingSearchForm_search"]').click()

    download_button=browser.find_element_by_xpath('//*[@id="back"]').click()

    time.sleep(3)
    filename = os.listdir(download_path)[0]
    newname=filename.replace("Semester Grade Card", os.environ.get('KTU_ID'))

    if filename.startswith("Semester"):
        print("File Downloaded")
        os.rename(os.path.join(download_path, filename), os.path.join(download_path, newname))
        
    print("File available in ",os.path.join(download_path, newname))
    
    return newname

