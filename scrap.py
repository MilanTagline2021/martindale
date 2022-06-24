import pandas as pd
import requests 
import time
from selenium.webdriver.common.by import By
from selenium import webdriver  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.maximize_window()
driver.get("https://www.martindale.com/")
time.sleep(5)
driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/section[4]/div/div[4]/div/div[1]/ul/li[1]/a').click()
time.sleep(1)

driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[1]/div/h1/span/a').click()
time.sleep(1)

get_url = driver.current_url

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

r = requests.get(get_url, headers=headers)
soup = BeautifulSoup(r.content)
g_data1=soup.find_all("li",{"class":"detail_title"})

name = []
title = []
company = []
address = []
phone = []
fax = []
profile = []
law_school = []
isln = []

for i in g_data1:
    k = i.find("a", href=True)
    if k:
        driver.get(k['href'])
        name.append(driver.find_element(By.CSS_SELECTOR, 'body > div.off-canvas-wrap > div > div.attorney-profile-content.profile-content > section.top-section > div.row.profile-title__container > div > h1').text)
        try:
            title.append(driver.find_element(By.CSS_SELECTOR, 'body > div.off-canvas-wrap > div > div.attorney-profile-content.profile-content > section.top-section > div.row.masthead-content.masthead-content-attorney > div.small-12.medium-6.large-7.columns.masthead-summary-container > ul > li.masthead-list__item.masthead-list__item--bold').text)
        except:
            title.append("")
        try:
            company.append(driver.find_element(By.CSS_SELECTOR, 'body > div.off-canvas-wrap > div > div.attorney-profile-content.profile-content > section.top-section > div.row.masthead-content.masthead-content-attorney > div.small-12.medium-6.large-7.columns.masthead-summary-container > ul > li.masthead-list__item.masthead-list__item--bold > a > span').text)
        except:
            company.append("")
        try:
            address.append(driver.find_element(By.CSS_SELECTOR, 'body > div.off-canvas-wrap > div > div.attorney-profile-content.profile-content > section.top-section > div.row.masthead-content.masthead-content-attorney > div.small-12.medium-6.large-7.columns.masthead-summary-container > ul > li:nth-child(2) > address').text)
        except:
            address.append("")
        phone.append(driver.find_element(By.CSS_SELECTOR, '#education-section > div > div > div:nth-child(1) > div.small-12.medium-9.columns.experience-value > span:nth-child(1)').text)
        try:
            fax.append(driver.find_element(By.CSS_SELECTOR, '#education-section > div > div > div:nth-child(1) > div.small-12.medium-9.columns.experience-value > span:nth-child(4)').text)
        except:
            fax.append("")
        
        try:
            profile.append(driver.find_element(By.CSS_SELECTOR, '#education-section > div > div > div:nth-child(1) > div.small-12.medium-9.columns.experience-value > a[href]').text)
        except:
            profile.append("")
        
        try:
            law_school.append(driver.find_element(By.CSS_SELECTOR, '#education-section > div > div > div:nth-child(3) > div.small-12.medium-9.columns.experience-value').text)
        except:
            law_school.append("")
        try:
            isln.append(driver.find_element(By.CSS_SELECTOR, '#education-section > div > div > div:nth-child(8) > div.small-12.medium-9.columns.experience-value').text)
        except:
            try:
                isln.append(driver.find_element(By.CSS_SELECTOR, '#education-section > div > div > div:nth-child(7) > div.small-12.medium-9.columns.experience-value').text)
            except:
                isln.append("")

        time.sleep(15)

dict = {'Name': name, 'Title': title, 'Company': company, 'Address': address, 'Phone': phone, 'Fax': fax, 'Profile': profile, 'Law School Attended':law_school, 'ISLN': isln} 
df = pd.DataFrame(dict)
df.to_csv(r'/Users/tagline/Downloads/file3.csv', index=False)
