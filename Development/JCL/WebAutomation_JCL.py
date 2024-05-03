from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import re
import os
import pandas as pd
from datetime import datetime
import zipfile
import mysql.connector

import sys
nric = sys.argv[1]
print("NRIC :", nric)
#exit()

# local database connection
# cnx = mysql.connector.connect(
#     host='localhost', user='root', password='', database='webform', port='5306')

# cnx = mysql.connector.connect(
#     host='149.28.139.83', 
#     user='crm', 
#     password='Crm536442.', 
#     database='crm_002_db', 
#     port='3306')

cnx = mysql.connector.connect(
    host='149.28.139.83',
    user='sharedAccount',
    password='Shared536442.',
    database='crm_002_db',
)

try:
    PATH = "/snap/chromium/2529/usr/lib/chromium-browser/chromedriver"
    service = Service(PATH)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    driver.get("https://jaccess.jclonline.my/JACCESS/login.php")
    print("Running")
    username = "MOTOSING_HQMN"
    password = "Mscr1963#"

    # username and Password
    wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div[1]/div[4]/table/tbody/tr[1]/td[2]/input")))
    driver.find_element(
        By.XPATH, "/html/body/div/div[1]/div[4]/table/tbody/tr[1]/td[2]/input").send_keys(username)
    driver.find_element(
        By.XPATH, "/html/body/div/div[1]/div[4]/table/tbody/tr[2]/td[2]/input[1]").send_keys(password)

    # login
    driver.find_element(
        By.XPATH, "/html/body/div/div[1]/div[4]/table/tbody/tr[3]/td/input").click()

    # Reload page
    driver.execute_script('location.reload(true)')

    # log out all devices
    new_application = "/html/body/input"
    logout_all = '/html/body/div/form/input[3]'

    def check_exist():
        try:
            driver.find_element(By.XPATH, logout_all)
            return True
        except NoSuchElementException:
            return False

    if check_exist():
        driver.find_element(By.XPATH, logout_all).click()
        driver.switch_to.frame(driver.find_element(
            By.CLASS_NAME, "icontabFrame"))
        wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/input")))
        driver.find_element(By.XPATH, new_application).click()
    # New Application
    else:
        print("New Application")
        driver.switch_to.frame(driver.find_element(
            By.CLASS_NAME, "icontabFrame"))
        wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/input")))
        driver.find_element(By.XPATH, new_application).click()

    # Continue
    # driver.find_element(
    #     By.XPATH, "/html/body/div[5]/div/div[3]/div[2]/button").click()

    # nric = "020620140951"
    # nric = nric
    # query that retrieve data from MySQL
    query = f"SELECT `Personal Info`.Name, `Personal Info`.Race, `Personal Info`.NRIC, `Personal Info`.Email, \
        `Personal Info`.Address, `Personal Info`.`Phone Number`, `Personal Info`.`Ownership Status`, `Personal Info`.`Marital Status`, \
        `Personal Info`.`No of year in residence`, `Banking Info`.`Bank Name`, `Banking Info`.`Type Of Account`, \
        `Banking Info`.`Bank Account Number`, `Extra Info`.`Best time to contact` FROM `Personal Info` \
        JOIN `Banking Info` ON `Personal Info`.NRIC = `Banking Info`.NRIC \
        JOIN `Extra Info` ON `Personal Info`.NRIC = `Extra Info`.NRIC \
        WHERE `Personal Info`.NRIC = {nric} LIMIT 1"
    # data = pd.read_excel(
    #     r"C:\Users\jerwo\AppData\Roaming\Python\Python310\site-packages\selenium\personal-project\Loan_App_2023.xlsx", dtype=str)
    # data = data.dropna(how='all').head(n=-1)
    data = pd.read_sql(query, cnx)
    print(data)
    print("Data retrieved")

    # Switch tab
    print('Switch to next tab')
    handles = driver.window_handles
    driver.switch_to.window(handles[1])

    # Full name
    print('Start first page')
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/input")))
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/input").send_keys(data['Name'])

    # Race
    chinese = "document.querySelector('.dropdown-content.select-dropdown.active li:nth-child(2) span').click()"
    indian = "document.querySelector('.dropdown-content.select-dropdown.active li:nth-child(3) span').click()"
    malay = "document.querySelector('.dropdown-content.select-dropdown.active li:nth-child(4) span').click()"
    others = "document.querySelector('.dropdown-content.select-dropdown.active li:nth-child(5) span').click()"

    driver.execute_script(
        "document.querySelector('.select-wrapper input.select-dropdown').click()")

    race = data['Race'].item()
    if race == 'Chinese':
        driver.execute_script(chinese)
    elif race == "Indian":
        driver.execute_script(indian)
    elif race == "Malay":
        driver.execute_script(malay)
    elif race == "Others":
        driver.execute_script(others)

    # NRIC
    driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div/div/input').send_keys(data['NRIC'])

    # Housing status
    companys_apartment = '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/ul/li[2]/span'
    familys_property = '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/ul/li[3]/span'
    parents_property = '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/ul/li[4]/span'
    own_property = '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/ul/li[6]/span'
    renting = '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/ul/li[5]/span'

    driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/input').click()

    # wait for dropdown box to appear
    sleep(1)

    ownershipStatus = data['Ownership Status'].item()
    if ownershipStatus == 'employer quarters':
        driver.find_element(By.XPATH, companys_apartment).click()
    elif ownershipStatus == 'family home':
        driver.find_element(By.XPATH, familys_property).click()
    elif ownershipStatus == 'parents home':
        driver.find_element(By.XPATH, parents_property).click()
    elif ownershipStatus == 'own mortgaged':
        driver.find_element(By.XPATH, own_property).click()
    elif ownershipStatus == 'rented':
        driver.find_element(By.XPATH, renting).click()

    # Marital status
    driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[8]/div/div/input').click()

    maritalStatus = wait.until(EC.visibility_of_element_located(
        (By.XPATH, f"//span[text()=\'{data['Marital Status'].item().upper()}\']")))
    maritalStatus.click()

    def scroll_down(element, amount):
        driver.execute_script("arguments[0].scrollTop += arguments[1];", element, amount)

    def scrollToFindAndClick(selectionBox, targetedXPath):
        while True:
            try:
                option = selectionBox.find_element(By.XPATH, targetedXPath)
                if option.is_displayed():
                    break
            except NoSuchElementException:
                scroll_down(selectionBox, 250)
                sleep(1)
                pass
        option.click()

    # Bank Name
    dataBankName = data['Bank Name'].item()
    cleanBankName = dataBankName.replace("BHD", "BERHAD")
    cleanBankName = re.sub(r'\W+','',cleanBankName)

    driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[9]/div/div/input').click()
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[9]/div/div/ul')))
    bankSelectionBox = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[9]/div/div/ul")
    # extract all bank names, clean them and compare to incoming data
    li_elements = bankSelectionBox.find_elements(By.XPATH,"./li")
    bankSelectionNames = [li.find_element(By.XPATH,"./span").text for li in li_elements]
    cleaned_values = [value.replace("BHD","BERHAD") for value in bankSelectionNames]
    cleaned_values = [re.sub(r'\W+','',value) for value in cleaned_values]
    targetText = ""
    for index, bankName in enumerate(cleaned_values):
        if bankName == cleanBankName:
                targetText = bankSelectionNames[index]
                break

    scrollToFindAndClick(bankSelectionBox, f"//li/span[text()='{targetText}']")

    # Type of Account
    current = '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/ul/li[2]/span'
    saving = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/ul/li[3]/span"

    driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/input').click()
    
    # wait for dropdown box
    sleep(1)

    typeOfAccount = data['Type Of Account'].item().lower()
    if typeOfAccount == 'current':
        driver.find_element(By.XPATH, current).click()
    elif typeOfAccount == 'saving':
        driver.find_element(By.XPATH, saving).click()

    # Account Num
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[11]/div/div/input").send_keys(data['Bank Account Number'].item())

    print('End first page')
    # Proceed button
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()
    sleep(3)

    print('Start second page')
    # Email Address
    wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/input")))
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/input").send_keys(data['Email'])

    # HandPhone No
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/input").send_keys(data['Phone Number'].item()[2::])
    sleep(1)

    # Address 1,2
    address = data['Address'].item()
    address_pattern = r"^(.*),?\s*\d{5}(?:(?:-|\s*)\d{4})?.*$"
    postal_code_pattern = r"\d{5}(?:(?:-|\s*)\d{4})?"
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[4]/div/div/input").send_keys(re.search(address_pattern, address).group(1))
    sleep(1)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[6]/div/div/input").send_keys(re.search(postal_code_pattern, address).group())
    sleep(1)

    # Length of stay
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[9]/div/div/input").click()
    sleep(1)
    noOfYear = data['No of year in residence'].item()
    if noOfYear == "1-2" or noOfYear == "3-4":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[9]/div/div/ul/li[3]/span").click()
    elif noOfYear == "5-6" or noOfYear == "7-8" or noOfYear == "8-9":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[9]/div/div/ul/li[4]/span").click()
    elif noOfYear == ">10":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[9]/div/div/ul/li[5]/span").click()
    sleep(1)

    # Best time to Contact
    am_to_pm = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/ul/li[2]/span"
    pm_to_pm1 = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/ul/li[6]/span"
    pm_to_pm2 = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/ul/li[9]/span"
    pm_to_am = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/ul/li[11]/span"

    driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/input').click()
    sleep(1)
    bestTimeContact = data['Best time to contact'].item()
    if bestTimeContact == "8am to 12pm":
        driver.find_element(By.XPATH, am_to_pm).click()
    elif bestTimeContact == "12pm to 4pm":
        driver.find_element(By.XPATH, pm_to_pm1).click()
    elif bestTimeContact == "4pm to 8pm":
        driver.find_element(By.XPATH, pm_to_pm2).click()
    elif bestTimeContact == "8pm to 12am" or bestTimeContact.lower() == 'anytime':
        driver.find_element(By.XPATH, pm_to_am).click()
    sleep(1)

    print('End second page')
    # Proceed button
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()

    queryReferenceContact = f"SELECT * FROM `Reference Contact` WHERE NRIC = {data['NRIC'].item()}"

    df = pd.read_sql(queryReferenceContact, cnx)
    print(df)

    print('Start third page, start of first emergency contact')
    # Emergency Contact 1
    # Relationship
    driver.find_element(By.CLASS_NAME, "select-dropdown").click()
    sleep(1)
    relation1 = df.iloc[0, -1]
    if relation1 == "spouse" or relation1 == "children":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/ul/li[2]/span").click()
    elif relation1 == "siblings" or relation1 == "friends":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/ul/li[3]/span").click()
    elif relation1 == "parents" or relation1 == "relatives":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/ul/li[4]/span").click()

    sleep(1)
    # Fullname
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/input").send_keys(df.iloc[0, 2])
    sleep(1)

    # Stay with Applicant
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div/div/input").click()
    sleep(1)
    if df.iloc[0, 5].lower() == "no":
        address = df.iloc[0, 6]
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div/div/ul/li[3]/span").click()
        sleep(1)
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/input").send_keys(re.search(address_pattern, address).group(1))
        sleep(1)
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[7]/div/div/input").send_keys(re.search(postal_code_pattern, address).group())
        sleep(1)
    elif df.iloc[0, 5].lower() == "yes":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div/div/ul/li[2]/span").click()
        sleep(1)

    # Handphone
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[9]/div/div/input").send_keys(df.iloc[0, 4][2::])
    sleep(1)

    # Best time to contact
    am_to_pm = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/ul/li[2]/span"
    pm_to_pm1 = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/ul/li[6]/span"
    pm_to_pm2 = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[11]/div/div/ul/li[9]/span"
    pm_to_am = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/ul/li[11]/span"

    driver.find_element(
        By.CSS_SELECTOR, "#ECP1-A-newapp_ns > div.hpanel.hred.animated-panel.fadeInUp.applet > div > form > div:nth-child(20) > div > div > input").click()
    sleep(1)
    if bestTimeContact == "8am to 12pm":
        driver.find_element(By.XPATH, am_to_pm).click()
    elif bestTimeContact == "12pm to 4pm":
        driver.find_element(By.XPATH, pm_to_pm1).click()
    elif bestTimeContact == "4pm to 8pm":
        driver.find_element(By.XPATH, pm_to_pm2).click()
    elif bestTimeContact == "8pm to 12am" or bestTimeContact.lower() == 'anytime':
        driver.find_element(By.XPATH, pm_to_am).click()
    sleep(1)

    print('End of third page, first emergency contact')
    # Proceed
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()
    sleep(1)

    # Emergency Contact 2
    # RelationShip

    print('Start of fourth page, start of second emergency contact')
    driver.find_element(By.CLASS_NAME, "select-dropdown").click()
    sleep(1)
    relation2 = df.iloc[1, -1]
    if relation2 == "spouse" or relation2 == "children":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/ul/li[3]/span").click()
    elif relation2 == "siblings" or relation2 == "friends":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/ul/li[4]/span").click()
    elif relation2 == "relatives":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/ul/li[5]/span").click()
    elif relation2 == "parents":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/ul/li[6]/span").click()
    else:
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/ul/li[2]/span").click()
    sleep(1)

    # FullName
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div/div/input").send_keys(df.iloc[1, 2])
    sleep(1)

    # Stay with applicant
    driver.find_element(
        By.CSS_SELECTOR, "#ECP2-A-newapp_ns > div.hpanel.hred.animated-panel.fadeInUp.applet > div > form > div:nth-child(15) > div > div > input").click()
    sleep(1)
    print(df.iloc[1, 5])
    if df.iloc[1, 5].lower() == "no":
        address = df.iloc[1, 6]
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[4]/div/div/ul/li[3]/span").click()
        sleep(1)
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/input").send_keys(re.search(address_pattern, address).group(1))
        sleep(1)
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[7]/div/div/input").send_keys(re.search(postal_code_pattern, address).group())
        sleep(1)
    elif df.iloc[1, 5].lower() == "yes":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[4]/div/div/ul/li[2]/span").click()
        sleep(1)

    # HandPhone No
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/input").send_keys(df.iloc[1, 4][2::])
    sleep(1)

    # Best time to Contact
    am_to_pm = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[11]/div/div/ul/li[2]/span"
    pm_to_pm = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[11]/div/div/ul/li[6]/span"
    pm_to_am = "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[11]/div/div/ul/li[11]/span"

    driver.find_element(
        By.CSS_SELECTOR, "#ECP2-A-newapp_ns > div.hpanel.hred.animated-panel.fadeInUp.applet > div > form > div:nth-child(22) > div > div > input").click()
    sleep(1)
    if bestTimeContact == "8am to 12pm":
        driver.find_element(By.XPATH, am_to_pm).click()
    elif bestTimeContact == "12pm to 4pm":
        driver.find_element(By.XPATH, pm_to_pm).click()
    elif bestTimeContact == "8pm to 12am" or bestTimeContact.lower() == 'anytime':
        driver.find_element(By.XPATH, pm_to_am).click()
    sleep(1)

    print('End fourth page, end of second emergency contact')
    # Proceed
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()

    # sql query for working info
    queryWorkingInfo = f"SELECT * FROM `Working Info` WHERE NRIC={data['NRIC'].item()}"
    dfWorkingInfo = pd.read_sql(queryWorkingInfo, cnx)
    print(dfWorkingInfo)

    # TODO: WILL CHANGE IN WEBFORM TO FIT WITH TYPE OF OCCUPATION
    # Employment Information
    # Type of occupation
    print('Start fifth page')

    # occupation from dataframe
    occupation = dfWorkingInfo['Position'].item().lower().strip()

    # occupation map for input search
    occupationMap = {
        "manager / supervisor" : "supervisor",
        "admin" : "admin",
        "factory worker" : "general worker",
        "general worker" : "general worker",
        "general manager / assistant" : "assistant manager",
        "saleman / promoter" : "sales",
        "managing director" : "management",
        #"officer / executive" : "executive", got 3 selection, so need to put in special case
        "pensioner / retiree" : "general worker",
        "professional ( lawyer, doctor )" : "lawyer",
        "skill worker ( technician / nurse )" : "technician",
        "teacher / lecture" : "teacher",
    } 

    # dropdown
    driver.find_element(
        By.XPATH, "//*[@id='EMPT_INFO-A-newapp_ns']/div[2]/div/form/div[1]/div/span/span[1]/span").click()
    sleep(1)

    # input search box
    searchBox = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")

    # input the corresponding nature business and select the first one
    if occupation in occupationMap:
        searchBox.send_keys(occupationMap[occupation])
        sleep(0.5)
        driver.find_element(
            By.XPATH, "/html/body/span/span/span[2]/ul/li").click()
    # special case for officer / executive
    elif occupation == "officer / executive":
        searchBox.send_keys("executive")
        sleep(0.5)
        driver.find_element(
            By.XPATH, "/html/body/span/span/span[2]/ul/li[3]").click()
    elif occupation == "other":
        print("End of Automation")
        print("Occupation: OTHERS - Please Rectify")
        exit()
    else:
        print(f"Unexpected Occupation value: {occupation}")
        exit()
    sleep(1)


    # TODO: WILL CHANGE IN WEBFORM TO FIT WITH BUSINESS NATURE
    # Nature of Business

    businessNature = dfWorkingInfo['Business Nature'].item().lower().strip()

    # business nature map for input search
    businessNatureMap = {
        "administrator / support services": "services",
        "agriculture": "agriculture",
        "arts / entertainment / recreation": "self employed",
        "banking / finance": "finance",
        "construction": "construction",
        "education": "services",
        "extraterritorial organization and bodies": "government",
        "healthcare": "services",
        "investment": "finance",
        "it / research / development": "telecommunication",
        "logistic": "logistic",
        "manufacturing": "manufacture",
        "mass media": "telecommunication",
        "mining / quarrying": "agriculture",
        "electrical": "telecommunication",
        "other services activities": "services",
        "production of domestic / personal services": "self employed",
        "retail / wholesale": "retail",
        "government": "government",
        "service line ( hotel, restaurants )": "services",
        "water supply / sewerage / waste management": "telecommunication"
    }

    # dropdown box
    driver.find_element(
        By.XPATH, "//*[@id='EMPT_INFO-A-newapp_ns']/div[2]/div/form/div[2]/div/span/span[1]/span").click()
    sleep(1)

    # input search box
    searchBox = driver.find_element(By.XPATH, "/html/body/span/span/span[1]/input")

    # input the corresponding nature business and select the first one
    if businessNature in businessNatureMap:
        searchBox.send_keys(businessNatureMap[businessNature])
        sleep(0.5)
        driver.find_element(
            By.XPATH, "/html/body/span/span/span[2]/ul/li").click()
    elif businessNature == "other":
        print("End of Automation")
        print("Business Nature: OTHERS - Please Rectify")
        exit()
    else:
        print(f"Unexpected Business Nature value: {businessNature}")
        exit()
    sleep(1)

    # Years of Service, Months of Service
    queryWorkingInfo = f"SELECT * FROM `Working Info` WHERE NRIC={data['NRIC'].item()}"
    dfWorkingInfo = pd.read_sql(queryWorkingInfo, cnx)

    yearMonth = dfWorkingInfo.iloc[0, 11].split('-')
    yearOfSerivce = datetime(int(yearMonth[0]), int(yearMonth[1]), 1)
    today = datetime.now()
    difference = today - yearOfSerivce

    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div[1]/div/input").send_keys(difference.days // 365)
    sleep(1)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div[2]/div/input").send_keys((difference.days % 365) // 30)
    sleep(1)

    # Salary Date
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[4]/div/span/span[1]/span/span[2]").click()
    sleep(1)
    driver.find_element(
        By.XPATH, "/html/body/span/span/span[1]/input").send_keys(dfWorkingInfo.iloc[0, -1])
    driver.find_element(
        By.XPATH, "/html/body/span/span/span[1]/input").send_keys(Keys.ENTER)
    sleep(1)

    # Net Salary
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/span/span").click()
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[5]/div/div/input").send_keys(dfWorkingInfo.iloc[0, -2])
    sleep(1)

    # Employment Type
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[6]/div/div/input").click()
    sleep(1)
    employmentType = dfWorkingInfo.iloc[0, 2].lower()
    if employmentType == "employed":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[6]/div/div/ul/li[3]/span").click()
    elif employmentType == "self-employed":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[6]/div/div/ul/li[5]/span").click()
    sleep(1)

    # Work Oversea
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[7]/div/div/input").click()
    sleep(1)
    workOverSea = dfWorkingInfo.iloc[0, 9].lower()
    if workOverSea == "no":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[7]/div/div/ul/li[2]/span").click()
    elif workOverSea == "yes":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[7]/div/div/ul/li[3]/span").click()
    sleep(1)

    # Company Name
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[8]/div/div/input").send_keys(dfWorkingInfo.iloc[0, 7])
    sleep(1)

    # Office Address 1,2,Postal Code,Tel No
    address = dfWorkingInfo.iloc[0, 10]
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[9]/div/div/input").send_keys(re.search(address_pattern, address).group(1))
    sleep(1)
    # driver.find_element(
    #     By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[10]/div/div/input").send_keys()
    # sleep(1)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[11]/div/div/input").send_keys(re.search(postal_code_pattern, address).group())
    sleep(1)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[14]/div/div/input").send_keys(dfWorkingInfo.iloc[0, 8][2::])
    sleep(1)

    print('End fifth page')
    # Proceed
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()

    print('Start sixth page')
    print("Start product selection")
    # Product group
    sleep(3)
    driver.find_element(By.CLASS_NAME, "select-dropdown").click()
    sleep(3)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/ul/li[2]").click()
    sleep(1)

    # TODO: WILL WAIT FOR CRM FOR THIS
    # Product
    driver.find_element(
        By.XPATH, "//*[@id='PROD-A-newapp_ns']/div[2]/div/form/div[2]/div/div/input").click()
    sleep(1)
    # if data.iloc[i, 22] == "new":
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/ul/li[2]/span").click()
    # elif data.iloc[i, 22] == "used":
    #     driver.find_element(
    #         By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/ul/li[3]/span").click()
    sleep(1)
    print("End of product selection")

    print("Start of Device/Motor Details")
    # Proceed
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()

    queryBrandModal = f"SELECT * FROM `Product Info` WHERE NRIC='{data['NRIC'].item()}'"
    dfBrandModal = pd.read_sql(queryBrandModal, cnx)
    # Device/Motor Details
    driver.find_element(By.ID, "COL-P_BRAND").click()
    sleep(1)
    driver.find_element(By.ID, "lens_FC_P_BRAND").send_keys(
        dfBrandModal['Brand'].item())
    # Cash Price
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/form/table/tbody/div[1]/tr[3]/div/td[2]/input").click()
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/form/table/tbody/div[1]/tr[3]/div/td[2]/input").send_keys(Keys.BACKSPACE)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/form/table/tbody/div[1]/tr[3]/div/td[2]/input").send_keys(dfBrandModal['Price'].item())
    sleep(1)

    # Description and Model No
    model = dfBrandModal['Model'].item()
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/form/table/tbody/div[1]/tr[4]/div/td[2]/span").click()
    sleep(1)
    modelSelectionBox = driver.find_element(By.XPATH, "/html/body/span/span/span[2]/ul")
    sleep(1)
    inputSearch = driver.find_element(
        By.XPATH, "/html/body/span/span/span[1]/input")
    inputSearch.click()
    inputSearch.send_keys(model)
    sleep(1)
    driver.find_element(By.XPATH, "/html/body/span/span/span[2]/ul/li[1]").click()
    sleep(1)

    print("End Device/Motor Details")

    # Add, Proceed
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div[2]/div/form/table/tbody/div[2]/a").click()
    sleep(3)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()

    print("Start Product Information (Payment information)")
    # Product Information
    # Tenary
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/input").click()
    sleep(1)
    tenure = dfBrandModal['Tenure'].item()[0:2]
    if tenure == "60":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/ul/li[6]").click()
    elif tenure == "48":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/ul/li[5]/span").click()
    elif tenure == "36":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/ul/li[4]/span").click()
    elif tenure == "24":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/ul/li[3]/span").click()
    elif tenure == "12":
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/ul/li[2]/span").click()
    sleep(1)

    # Down Payment
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div/div/input").click()
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[3]/div/div/input").send_keys(dfBrandModal['Down Payment'].item())
    sleep(1)

    print("End product information")
    print('End sixth page ')
    # Proceed
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()

    print('Start seventh page')
    # Document Generation
    sleep(1.2)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/div[2]/div[2]/a").click()
    sleep(4)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[1]/div/div/div[3]/div[2]/a").click()
    sleep(4)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[2]/div/form/div[2]/div/div/div/div").click()
    sleep(3)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()
    # delete downloaded files
    os.remove("Notice_1_HP_pdf.pdf")
    os.remove("Application_Form_HP_pdf.pdf")
    print("Deleted Downloaded Files")
    # Document Upload
    pdfQuery = f"SELECT pdfFilePath FROM `Banking Info` WHERE NRIC={data['NRIC'].item()}"
    dfPdf = pd.read_sql(pdfQuery, cnx)

    PDF_doc = dfPdf['pdfFilePath'].item()
    sleep(2)

    # application form
    # driver.find_element(
    #     By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[1]").click()
    if PDF_doc.endswith('.pdf'):
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/input").send_keys(os.path.abspath(PDF_doc))
        sleep(2)
    else:
        # server webform path
        webFormPath = "/Development/Webform/WEBFORM_Files"
        fullPath = os.path.join(webFormPath,os.path.normpath(PDF_doc))
        pdfFile = ""
        with zipfile.ZipFile(fullPath, 'r') as zip_ref:
            print("Unzipping :",zip_ref.filename)
            for file_name in zip_ref.namelist():
                if file_name.endswith('.pdf'):
                    pdfFile = zip_ref.extract(file_name)
                    print("Extracted :",pdfFile)
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[1]/div[2]/div[2]/input").send_keys(pdfFile)
        sleep(2)

    # latest payslip
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[2]").click()
    sleep(2)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[2]/div[2]/div[2]/input").send_keys(pdfFile)
    print("uploaded latest payslip")
    sleep(2)


    # latest utility bill
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[3]").click()
    sleep(2)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[3]/div[2]/div[2]/input").send_keys(pdfFile)
    sleep(2)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[4]").click()
    sleep(2)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[4]/div[2]/div[2]/input").send_keys(pdfFile)
    sleep(2)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[5]").click()
    sleep(2)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[5]/div[2]/div[2]/input").send_keys(pdfFile)
    sleep(2)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[6]").click()
    sleep(2)


    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div[1]/div[6]/div[2]/div[2]/input").send_keys(os.path.abspath(f"./{PDF_doc.split('.zip')[0].split('/')[-1]}.pdf"))
    sleep(2)

    # Proceed
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div[2]/div[4]/a[2]").click()

    # Acknowledgement
    sleep(1)
    print("Proceed with Acknowledgement")
    driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div/div/a").click()

    # delete extracted files
    print("Delete extracted pdfFile")
    os.remove(pdfFile)

    print('End seventh page')
    print("End of Automation")
    print("Input to continue")
    input()
except Exception as e:
    print(e)
    input()
