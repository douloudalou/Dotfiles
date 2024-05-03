# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from rich import print
import mysql.connector
import pandas as pd
import scrapy
from scrapy.utils.response import open_in_browser
from datetime import datetime
from dateutil import relativedelta
from zipfile import ZipFile
from pathlib import Path
from time import sleep
con = mysql.connector.connect(
    host='149.28.139.83',
    user='sharedAccount',
    password='Shared536442.',
    database='crm_002_db',
    port='3306'
)

class dcapSpider(scrapy.Spider):
    name = "dcap"
    allowed_domains = ["dcap.my"]
    
    login_url = "https://www.dcap.my/user/login"
    start_urls = [login_url]

    def parse(self, response):
        accountDetails = {
            '_token': response.css('input[name="_token"]::attr(value)').get(),
            'email': 'motsales1@dcap-los',
            'password': 'mot@888'
        }
        print(accountDetails)
        scriptType = input('Type: all/nric:')
        nric = None
        if scriptType == 'nric':
            nric = input('NRIC: ')
        yield scrapy.FormRequest(url=self.login_url, formdata=accountDetails, callback=self.application, meta={'index': nric})

    def application(self, response):
        print('-----------------------------')
        application_url = "https://www.dcap.my/user/application/add"
        index = response.meta['index']
        yield response.follow(url=application_url, callback=self.customerDetails, meta={'index': index})

    def customerDetails(self, response):
        print('---------------1-------------')
        application_url = "https://www.dcap.my/user/application/add"
        Personal_data = None
        index = response.meta['index']
        if index == None:
            Personal_data = pd.read_sql(f'Select * from `Personal Info`', con)
        else:
            Personal_data = pd.read_sql(f'Select * from `Personal Info` where `NRIC`="{index}"', con)

        for i in range(len(Personal_data)):
            address = (Personal_data['Address'][i]).split(',')
            formData = {
                '_token': response.css('input[name="_token"]::attr(value)').get(),
                'name': Personal_data['Name'][i],
                'nric_no': f"{Personal_data['NRIC'][i][0:6]}-{Personal_data['NRIC'][i][6:8]}-{Personal_data['NRIC'][i][8:]}",
                'mobile_number': f"{Personal_data['Phone Number'][i]}",
                'best_time_to_call_customer_from': '9:00 AM',
                'best_time_to_call_customer_to': '5:00 PM',
                'email_address': Personal_data['Email'][i],
                'gender': Personal_data['Gender'][i],
                'marital_status': (Personal_data['Marital Status'][i]).lower(),
                'race': (Personal_data['Race'][i]).lower(),
                'address_line_1': address[:2],
                'address_line_2': address[2],
                'city': address[4],
                'postcode': address[3],
                'state': (address[5].lower())[1:].replace(" ", "_"),
            }
            print(formData)
            yield scrapy.FormRequest(
                url=application_url,
                formdata=formData,
                callback=self.employment,
                meta={'index': Personal_data['NRIC'][i]},
                dont_filter=True
            )

    def employment(self, response):
        print('---------------2-------------')
        index = response.meta['index']
        employment_url = response.css('form[method="POST"]::attr(action)').get()
        Working_data = pd.read_sql(f'Select * from `Working Info` where `NRIC`="{index}"', con)
        Banking_data = pd.read_sql(f'Select * from `Banking Info` where `NRIC`="{index}"', con)

        # Employment length
        now = datetime.now()
        date_1 = datetime(2022, 1, 1)
        date_2 = datetime(int(now.strftime('%Y')), int(now.strftime('%m')), 1)
        diff = relativedelta.relativedelta(date_2, date_1).years
        if diff > 5:
            diff = 4
        elif diff >= 3|4|5:
            diff = 3
        elif diff == 2:
            diff = 2
        else:
            diff = 1

        # Employment segment
        array = {
            'gig': ['other services activities', 'production of domestic / personal services'],
            'police': [],
            'government_staff_26' : ['extraterritorial organization and bodies', 'government'],
            'driver_27' : [],
            'security_guard_28' : ['other'],
            'semi-skilled_29' : ['construction', 'logistic', 'manufacturing', 'mining / quarrying', 'electrical', 'water supply / sewerage / waste management'],
            'retail_30' : ['retail / wholesale', 'service line ( hotel, restaurants )'],
            'office_workers_admin_clerk_hr_31' : ['administrator / support services'],
            'professional_32' : ['agriculture', 'arts / entertainment / recreation', 'banking / finance', 'education', 'healthcare', 'investment', 'IT / research / development', 'mass media'],
        }
        
        def segment(z, x):
            for i in x:
                if z in x[i]:
                    return i

        employment_segment = segment(Working_data['Business Nature'][0], array)

        # Address
        address = (Working_data['Company Address'][0]).split(',')

        # Bank
        allBank = response.css('option::text').getall()
        def bank(n):
            for i in allBank:
                if n.lower().replace('berhad', '') in i.lower().replace('berhad', ''):
                    return response.css(f'option:contains("{i}")::attr(value)').get()
                if n == 'PUBLIC BANK/PUBLIC FINANCE BERHAD':
                    return 'public'
                # if i.lower() == n.lower():
                #     return response.css(f'option:contains("{i}")::attr(value)').get()
                # elif ('Hong Leong Bank').lower() == n.lower():
                #     return 'hong_leong'

        formData = {
            '_token': response.css('input[name="_token"]::attr(value)').get(),
            'occupation': Working_data['Position'][0],
            'occupation_type': Working_data['Employment Status'][0].lower().replace('-', '_'),
            'employment_length': str(diff),
            'employment_segment': employment_segment,
            'employer_name': Working_data['Company Name'][0],
            'employer_telephone_number': Working_data['Company Phone Number'][0],
            'alternate_employer_telephone_number': '+60128887213', #
            'employer_best_time_to_call_from': '9:00 AM',
            'employer_best_time_to_call_to': '5:00 PM',
            'employer_address1': address[:2],
            'employer_address2': address[2],
            'employer_city': address[4],
            'employer_postcode': address[3],
            'employer_state': (address[5].lower())[1:].replace(" ", "_"),
            'gross_salary': '4000',#Working_data['Gross Salary'][0].split(' ')[1], 
            'net_salary':  '2499',#Working_data['Net Salary'][0].split(' ')[1],
            'salary_crediting_bank': bank(Banking_data["Bank Name"][0]),
            'salary_crediting_acc_no': Banking_data['Bank Account Number'][0],
            'salary_crediting_day': Working_data['Salary Term'][0],
            'epf': Working_data['Have EPF'][0].lower()
        }
        print(formData)
        yield scrapy.FormRequest(
                url=employment_url,
                formdata=formData,
                callback=self.reference,
                meta={'index': index},
                dont_filter=True
        )

    def reference(self, response):
        print('---------------3-------------')
        index = response.meta['index']
        reference_url = response.css('form[method="POST"]::attr(action)').get()
        reference_data = pd.read_sql(f'Select * from `Reference Contact` where `NRIC`="{index}"', con)

        print(reference_data)
        formData = {
            '_token': response.css('input[name="_token"]::attr(value)').get(),
            'ref_1_name': reference_data['Name'][0],
            'ref_1_nric': f"{reference_data['Reference Contact NRIC'][0][0:6]}-{reference_data['Reference Contact NRIC'][0][6:8]}-{reference_data['Reference Contact NRIC'][0][8:]}",
            'ref_1_contact_no': reference_data['Phone Number'][0],
            'ref_1_relationship_with_applicant': reference_data['Relation to user'][0],
            'ref_2_name': reference_data['Name'][1],
            'ref_2_nric': f"{reference_data['Reference Contact NRIC'][1][0:6]}-{reference_data['Reference Contact NRIC'][1][6:8]}-{reference_data['Reference Contact NRIC'][1][8:]}",
            'ref_2_contact_no': reference_data['Phone Number'][1],
            'ref_2_relationship_with_applicant': reference_data['Relation to user'][1]
        }
        print(formData)
        yield scrapy.FormRequest(
                url=reference_url,
                formdata=formData,
                callback=self.finance,
                meta={'index': index},
                dont_filter=True
        )

    def finance(self, response):
        print('---------------4-------------')
        index = response.meta['index']
        finance_url = response.css('form[method="POST"]::attr(action)').get()
        product_data = pd.read_sql(f'Select * from `Product Info` where `NRIC`="{index}"', con)

        # Tenure
        Tenure=''
        if int(product_data['Tenure'][0].split(' ')[0]) > 48:
            Tenure = '48'
        elif int(product_data['Tenure'][0].split(' ')[0])==12:
            Tenure = '24'
        else:
            Tenure = product_data['Tenure'][0].split(' ')[0]
        
        print(product_data)
        formData = {
            '_token': response.css('input[name="_token"]::attr(value)').get(),
            'product_id': '17',
            'condition': 'New',
            'new_model_id': '275', #
            'text_sale_price': '10000', #
            'deposit': '2000', #
            'financing_amount': str(10000-2000), #
            'interest_rate': '10.00',
            'new_tenure': Tenure
        }
        print(formData)
        yield scrapy.FormRequest(
                url=finance_url,
                formdata=formData,
                callback=self.attachment,
                meta={'index': index},
                dont_filter=True
        )

    # def openPDF(self, file, selenium_path):
    #     import os
    #     path = os.path.abspath(file)
    #     print(path)
    #     selenium_path.send_keys(path)

    def attachment(self, response):
        print('---------------5-------------')
        attachment_url = response.css('form[method="POST"]::attr(action)').get()
        import os
        zipFileName = f"{response.meta['index']}.zip"
        zipPath = Path(f"/Development/Automation/dcapSpider/spiders/pdfFiles/{zipFileName}")
        extractPath = Path(r"/Development/Automation/dcapSpider/spiders/extractFiles")

        with ZipFile(zipPath, 'r') as zip:
            print(f"{zip} extracted")
            zip.extractall(extractPath)

        file = str(Path(extractPath) / f"{response.meta['index']}.pdf")
        print(file)
        print(os.path.exists(file))
        from scrapy_selenium import SeleniumRequest
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver import Chrome
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        
        driver = Chrome(executable_path='/snap/bin/chromium.chromedriver', options=chrome_options)
        driver.get(self.login_url)
        
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/form/div[2]/input'))).send_keys('motsales1@dcap-los')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/form/div[3]/input'))).send_keys('mot@888')
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/form/button'))).click()
        driver.get(attachment_url)
        
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nric_front"]'))).send_keys(file)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nric_back"]'))).send_keys(file)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="income_doc"]'))).send_keys(file)
        # WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="attachment-form"]/div[15]/div/button[2]'))).click()
        
        yield SeleniumRequest(
                url=attachment_url
        )



    # def file(self, file):
    #     import os
    #     path = os.path.abspath(file)
    #     print(path)
    #     return path

    # def attachment(self, response):
    #     print('---------------5-------------')
    #     attachment_url = response.css('form[method="POST"]::attr(action)').get()
    #     import os
    #     import requests
    #     zipFileName = f"{response.meta['index']}.zip"
    #     zipPath = Path(f"/home/Meee/Development/dcapSpider/spiders/pdfFiles/{zipFileName}")
    #     extractPath = Path(r"/home/Meee/Development/dcapSpider/spiders/extractFiles")

    #     with ZipFile(zipPath, 'r') as zip:
    #         print(f"{zip} extracted")
    #         zip.extractall(extractPath)

    #     file = str(Path(extractPath) / f"{response.meta['index']}.pdf")
    #     print(file)
    #     print(os.path.exists(file))

    #     from selenium.webdriver.common.by import By
    #     from selenium.webdriver.support import expected_conditions as EC
    #     from selenium.webdriver.support.ui import WebDriverWait
    #     from selenium.webdriver import Chrome
    #     from selenium.webdriver.chrome.options import Options
    #     chrome_options = Options()
    #     # chrome_options.add_argument('--headless')
    #     chrome_options.add_argument('--no-sandbox')
    #     # executable_path='/usr/bin/chromedriver', options=chrome_options
    #     driver = Chrome()
    #     driver.get(self.login_url)
        
    #     WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/form/div[2]/input'))).send_keys('motsales1@dcap-los')
    #     WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/form/div[3]/input'))).send_keys('mot@888')
    #     WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/form/button'))).click()
    #     driver.get(attachment_url)

    #     files = {
    #         'nric_front': file,
    #         'nric_back': file,
    #         'income_doc': file
    #     }
        
        
    #     response = requests.post(attachment_url, files=files)
    #     print(response.status_code)
    #     sleep(3)

    #     # Close the file handles
    #     for file_handle in files.values():
    #         file_handle.close()

# EOF





