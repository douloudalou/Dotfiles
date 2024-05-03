from rich import print
import scrapy
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from openpyxl import load_workbook
import pandas as pd

class Mobius(scrapy.Spider):
    name = "Mobius"
    
    login_url = "https://mv.mobius.sg/"
    start_urls = [login_url]

    def __init__(self):
        #Excel 
        file = r'/home/Meee/Mobius/Profile.xlsx'
        book = load_workbook(file)
        writer = pd.ExcelWriter(file, engine='openpyxl', mode='a', if_sheet_exists='overlay')
        workbook = writer.book

        self.driver = Chrome()
        self.driver.get(self.login_url)
        wait = WebDriverWait(self.driver, 10)

        sheet = (input("sheet: ")).upper()
        classType = (input("class (3, 4): ")).upper()
        data = pd.read_excel(r'/home/Meee/Mobius/Profile.xlsx', sheet)
        
        # try:
        # click resourse
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[35]/div[1]/div/div[3]'))).click()
        # click dashboard
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[35]/div[1]/div/div[4]/div/div/div[2]/label'))).click()
        # swtich to resource page iframe
        sleep(5)
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '/html/body/div[35]/div[2]/iframe'))
        # click TO
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div'))).click()
        # swtich to resource iframe
        sleep(5)
        self.driver.switch_to.frame(self.driver.find_element(By.XPATH, '/html/body/iframe'))

        excluded = ['BMTV (SCH V)', '1TPT (NORTH)', '3TPT (CENTRAL)', 'TPT HUB (EAST)', 'TPT HUB (WEST)', 'BA65']

        for r in data.iterrows():
            print(str(r[1]))
            sleep(5)
            # click new driver
            print(self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[9]/div/label'))
            sleep(3)
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[9]/div/label'))).click()
            
            ##### FORM #####
            # Role: TO, if  cadet TL
            role = ''
            if ((str(r[1]['Unit'])) not in excluded):
                role = 'DV'
            else:
                if ((str(r[1]['Rank'])) == 'SCT'):
                    role = 'TL'
                else:
                    role = 'TO'
            wait.until(EC.element_to_be_clickable((By.XPATH, f'//select[@name="role"]/option[text()="{role}"]'))).click()
            # Vocation: Trainee
            vocation = ''
            if ((str(r[1]['Unit'])) in excluded):
                if ((str(r[1]['Unit'])) == 'BMTV (SCH V)'):
                    if classType == '3':
                        vocation = 'BASE (Trainee)'
                    else:
                        vocation = 'CS/CSS (Trainee)'
                elif ((str(r[1]['Rank'])) == 'SCT'):
                    vocation = 'Trainee'
                else:
                    vocation = 'CBT (Trainee)'
                wait.until(EC.element_to_be_clickable((By.XPATH, f'//select[@name="Vocation"]/option[text()="{vocation}"]'))).click()
            else:
                wait.until(EC.element_to_be_clickable((By.XPATH, f'//select[@name="Vocation"]/option[text()="-"]'))).click()
            # Unit
            if ((str(r[1]['Unit'])) not in excluded):
                unit = (str(r[1]['Unit']))
                print(self.driver.find_element(By.XPATH, f'//select[@name="Unit"]/option[text()="{unit}"]'))
                sleep(5)
                wait.until(EC.element_to_be_clickable((By.XPATH, f'//select[@name="Unit"]/option[text()="{unit}"]'))).click()
            # Hub
            hub = ''
            if ((str(r[1]['Unit'])) in excluded):
                if ((str(r[1]['Unit'])) == 'BMTV (SCH V)' or ((str(r[1]['Unit'])) == 'BA65')):
                    hub = 'BA65'
                elif ((str(r[1]['Unit'])) == '1TPT (NORTH)'):
                    hub = 'BB71'
                elif ((str(r[1]['Unit'])) == '3TPT (CENTRAL)'):
                    hub = '602H'
                elif ((str(r[1]['Unit'])) == 'TPT HUB (EAST)'):
                    hub = 'BB70'
                elif ((str(r[1]['Unit'])) == 'TPT HUB (WEST)'):
                    hub = 'BB72'
                print(self.driver.find_element(By.XPATH, f'//select[@name="hub"]/option[text()="{hub}"]'))
                sleep(5)
                wait.until(EC.element_to_be_clickable((By.XPATH, f'//select[@name="hub"]/option[text()="{hub}"]'))).click()
            # Node
            node = (str(r[1]['Node']))
            if ((str(r[1]['Unit'])) in excluded):
                if ((str(r[1]['Node'])) != '0'):
                    print(node)
                    sleep(3)
                    wait.until(EC.element_to_be_clickable((By.XPATH, f'//select[@name="node"]/option[text()="{node}"]'))).click()
            # Date Of Enlistment
            print(self.driver.find_element(By.XPATH, '//*[@id="vehicle-info-form"]/div/div[1]/div[7]/input'))
            sleep(3)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vehicle-info-form"]/div/div[1]/div[7]/input'))).click()
            (currentDoeYr) = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[-2:]
            (currentDoeMh) = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[3:5]
            print(str(r[1]['Date of Enlistment']))
            doeYr = (str(r[1]['Date of Enlistment']))[-2:]
            doeMh = (str(r[1]['Date of Enlistment']))[3:5]
            doeDate = (str(r[1]['Date of Enlistment']))[:2]
            if doeDate.startswith('0'):
                doeDate = doeDate[1:] 
            print(currentDoeYr, currentDoeMh)
            print(doeYr, doeMh, doeDate)
            sleep(5)
            while (currentDoeYr != doeYr):
                if (currentDoeYr > doeYr):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[1]'))).click()
                    currentDoeYr = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[-2:]
                if (currentDoeYr < doeYr):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[4]'))).click()
                    currentDoeYr = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[-2:]
            while (currentDoeMh != doeMh):
                if (currentDoeMh > doeMh):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[2]'))).click()
                    currentDoeMh = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[3:5]
                if (currentDoeMh < doeMh):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[3]'))).click()
                    currentDoeMh = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[3:5]  
            sleep(5)
            wait.until(EC.element_to_be_clickable((By.XPATH, f'//td[div[text()="{doeDate}"]]'))).click()

            # Date of ORD
            print(self.driver.find_element(By.XPATH, '//*[@id="vehicle-info-form"]/div/div[1]/div[8]/input'))
            sleep(3)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vehicle-info-form"]/div/div[1]/div[8]/input'))).click()
            
            (currentDooYr) = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[-2:]
            (currentDooMh) = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[3:5]
            print(str(r[1]['Date of ORD']))
            dooYr = (str(r[1]['Date of ORD']))[-2:]
            dooMh = (str(r[1]['Date of ORD']))[3:5]
            dooDate = (str(r[1]['Date of ORD']))[:2]
            if dooDate.startswith('0'):
                dooDate = dooDate[1:] 
            print(currentDooYr, currentDooMh)
            print(dooYr, dooMh, dooDate)
            sleep(5)

            while (currentDooYr != dooYr):
                if (currentDooYr > dooYr):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[1]'))).click()
                    currentDooYr = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[-2:]
                if (currentDooYr < dooYr):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[4]'))).click()
                    currentDooYr = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[-2:]
            while (currentDooMh != dooMh):
                if (currentDooMh > dooMh):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[2]'))).click()
                    currentDooMh = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[3:5]
                if (currentDooMh < dooMh):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[3]'))).click()
                    currentDooMh = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[3:5]                 
            wait.until(EC.element_to_be_clickable((By.XPATH, f'//td[div[text()="{dooDate}"]]'))).click()

            # NRIC
            nric = r[1]['sgID Validated NRIC']
            self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div/form/div/div[3]/div[2]/input').send_keys(nric)
            # Driver Name
            name = r[1]['[MyInfo] Name']
            self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div/form/div/div[3]/div[3]/input').send_keys(name)
            # Contact number
            contact = int(r[1]['Mobile number'])
            self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div/form/div/div[3]/div[5]/input').send_keys(str(contact)[2:])
            
            # DOB
            print(self.driver.find_element(By.XPATH, '//*[@id="vehicle-info-form"]/div/div[3]/div[4]/input'))
            sleep(3)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vehicle-info-form"]/div/div[3]/div[4]/input'))).click()
            
            (currentDobYr) = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[-4:]
            (currentDobMh) = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[3:5]
            dobYr = (str(r[1]['[MyInfo] Date of birth']))[-4:]
            dobMh =(str(r[1]['[MyInfo] Date of birth']))[3:5]
            dobDate = (str(r[1]['[MyInfo] Date of birth']))[:2]
            if dobDate.startswith('0'):
                dobDate = dobDate[1:] 
            print(currentDobYr, currentDobMh)
            print(dobYr, dobMh, dobDate)
            sleep(5)
            while (currentDobYr != dobYr):
                if (currentDobYr > dobYr):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[1]'))).click()
                    currentDobYr = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[-4:]
                if (currentDobYr < dobYr):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[4]'))).click()
                    currentDobYr = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[-4:]
            while (currentDobMh != dobMh):
                if (currentDobMh > dobMh):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[2]'))).click()
                    currentDobMh = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[3:5]
                if (currentDobMh < dobMh):
                    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[1]/div[1]/i[3]'))).click()
                    currentDobMh = self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/span').get_attribute('innerHTML')[3:5]                  
            wait.until(EC.element_to_be_clickable((By.XPATH, f'//td[div[text()="{dobDate}"]]'))).click()
            sleep(3)
            # DONE
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/div[2]/div/label'))).click()
            # WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[2]/div/div/div/div/div/div/div/div[4]/button')))
            try:
                exist = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div[2]/div/div/div/div/div/div/div/div[4]/button')))
                print('Skip...')
                sleep(3)
                self.driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div/div/div/div/div/div/div/div[4]/button').click()
                self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/button').click()
                sleep(5)
            except TimeoutException:
                exist = False
                print('Created...')
                sleep(3)
                pass
            # print('Exist: ', exist)
            # sleep(5)
            # if (exist):
                
            # else:
                    
        # except:
        #     print(str(r[1]), exist)
        #     input('error...')
        input('DONE...')
        self.driver.quit()
